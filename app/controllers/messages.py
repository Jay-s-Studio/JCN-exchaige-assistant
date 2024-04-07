"""
MessagesController
"""
import asyncio
import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional
from uuid import UUID

import pytz
from telegram import Update, User
from telegram.constants import ParseMode

from app.libs.consts import messages
from app.libs.consts.enums import GinaAction, CurrencySymbol, OperationType, CalculationType, OrderStatus, Language, CartStatus
from app.libs.decorators.sentry_tracer import distributed_trace
from app.providers import ExchangeRateProvider, TelegramAccountProvider, HandlingFeeProvider, OrderProvider, VendorsBotProvider
from app.schemas.exchange_rate import OptimalExchangeRate
from app.schemas.gina import GinaResponse
from app.schemas.order import Order, Cart
from app.schemas.vendors_bot import PaymentAccount, ConfirmPayment
from app.serializers.v1.handling_fee import HandlingFeeConfigItem


@dataclass
class FormatOptions:
    """FormatOptions"""
    customer_service: bool = True


class MessagesController:
    """MessagesController"""

    def __init__(
        self,
        telegram_account_provider: TelegramAccountProvider,
        exchange_rate_provider: ExchangeRateProvider,
        handling_fee_provider: HandlingFeeProvider,
        order_provider: OrderProvider,
        vendors_bot_provider: VendorsBotProvider
    ):
        self._telegram_account_provider = telegram_account_provider
        self._exchange_rate_provider = exchange_rate_provider
        self._handling_fee_provider = handling_fee_provider
        self._order_provider = order_provider
        self._vendors_bot_provider = vendors_bot_provider

    @distributed_trace()
    async def on_exchange_rate(self, update: Update, gina_resp: GinaResponse) -> messages.Message:
        """
        on exchange rate
        :param update:
        :param gina_resp:
        :return:
        """
        match gina_resp.action:
            case GinaAction.EXCHANGE_RATE:
                message = await self._exchange_rate(update=update, gina_resp=gina_resp)
            case GinaAction.EXCHANGE_RATE_MAIN_TOKEN:
                message = await self._exchange_rate(update=update, gina_resp=gina_resp, get_default=True)
            case _:
                message = messages.Message(text=gina_resp.reply)
        return message

    @distributed_trace()
    async def _exchange_rate(self, update: Update, gina_resp: GinaResponse, get_default: bool = False) -> messages.Message:
        """
        exchange rate
        :param update:
        :param gina_resp:
        :param get_default:
        :return:
        """
        await update.effective_message.reply_text(text=gina_resp.reply)
        if get_default:
            group = await self._telegram_account_provider.get_chat_group(group_id=update.effective_chat.id)
            if not group.currency_symbol:
                return messages.DefaultCurrencyNotFoundMessage.format(language=gina_resp.language)
            payment_currency = group.currency_symbol
            exchange_currency = CurrencySymbol.USDT.value
        else:
            payment_currency = gina_resp.payment_currency.upper()
            exchange_currency = gina_resp.exchange_currency.upper()
            if exchange_currency == "G":
                exchange_currency = "GCASH"
            if exchange_currency == "M":
                exchange_currency = "PAYMAYA"

        exchange_rate, handling_fee = await self._get_rate_and_fee(
            group_id=update.effective_chat.id,
            currency=payment_currency if payment_currency != "USDT" else exchange_currency,
            operation_type=OperationType.BUY if payment_currency != "USDT" else OperationType.SELL
        )
        if not exchange_rate:
            return messages.ExchangeRateErrorMessage.format(
                language=gina_resp.language,
                payment_currency=payment_currency,
                exchange_currency=exchange_currency,
            )
        price = await self._get_price(
            exchange_rate=exchange_rate,
            handling_fee=handling_fee,
            operation_type=OperationType.BUY if payment_currency != "USDT" else OperationType.SELL
        )
        await asyncio.sleep(1.5)
        return messages.ExchangeRateMessage.format(
            language=gina_resp.language,
            payment_currency=payment_currency,
            exchange_currency=exchange_currency,
            price=price
        )

    @distributed_trace()
    async def on_swap(self, update: Update, gina_resp: GinaResponse) -> messages.Message:
        """
        on swap
        :param update:
        :param gina_resp:
        :return:
        """
        order_info = await self._order_provider.get_order_by_group_id(group_id=update.effective_chat.id)
        if order_info:
            if order_info.status not in [OrderStatus.EXPIRE, OrderStatus.DONE, OrderStatus.CANCELLED]:
                return messages.OrderInProgressMessage.format(language=gina_resp.language)
        match gina_resp.action:
            case GinaAction.SWAP:
                message = await self._swap(update=update, gina_resp=gina_resp)
            case GinaAction.SWAP_CRYPTO:
                message = await self._swap(update=update, gina_resp=gina_resp)
            case GinaAction.SWAP_LEGAL:
                message = messages.Message(text=gina_resp.reply)
            case _:
                message = messages.Message(text=gina_resp.reply)
        return message

    @distributed_trace()
    async def _swap(self, update: Update, gina_resp: GinaResponse) -> messages.Message:
        """
        swap
        :param update:
        :param gina_resp:
        :return:
        """
        group_id = update.effective_chat.id
        payment_currency = gina_resp.payment_currency
        exchange_currency = gina_resp.exchange_currency
        payment_amount = gina_resp.amount_to_exchange
        currency = payment_currency
        if exchange_currency == "G":
            currency = payment_currency = "GCASH"
            exchange_currency = "USDT"
        if exchange_currency == "M":
            currency = payment_currency = "PAYMAYA"
            exchange_currency = "USDT"
        if exchange_currency != "USDT":
            currency = exchange_currency

        # try to get cart by group id
        exist_cart = await self._order_provider.get_cart_by_group_id(group_id=group_id)
        if exist_cart:
            if exist_cart.payment_currency != payment_currency or exist_cart.exchange_currency != exchange_currency:
                return messages.CartCurrencyMismatchMessage.format(language=gina_resp.language)

            if payment_currency in ["GCASH", "PAYMAYA"]:
                payment_amount = self._round_to_nearest((Decimal(payment_amount) * Decimal("10000")))
            else:
                payment_amount = self._round_to_nearest((Decimal(payment_amount) * Decimal(exist_cart.with_fee_exchange_rate)))
            exchange_amount = self._round_to_nearest((Decimal(payment_amount) / Decimal(exist_cart.with_fee_exchange_rate)))

            exist_cart.payment_amount = float(self._round_to_nearest(Decimal(exist_cart.payment_amount) + payment_amount))
            exist_cart.exchange_amount = float(self._round_to_nearest(Decimal(exist_cart.exchange_amount) + exchange_amount))
            await self._order_provider.update_cart(cart=exist_cart)
            return messages.CartInfoMessage.format(
                language=gina_resp.language,
                payment_currency=exist_cart.payment_currency,
                exchange_currency=exist_cart.exchange_currency,
                exchange_rate=exist_cart.with_fee_exchange_rate,
                total_price=exist_cart.payment_amount,
                cart_id=exist_cart.id
            )

        exchange_rate, handling_fee = await self._get_rate_and_fee(
            group_id=group_id,
            currency=currency,
            operation_type=OperationType.BUY if payment_currency != "USDT" else OperationType.SELL
        )
        if not exchange_rate:
            return messages.ExchangeRateErrorMessage.format(
                language=gina_resp.language,
                payment_currency=payment_currency,
                exchange_currency=exchange_currency,
            )
        price = await self._get_price(
            exchange_rate=exchange_rate,
            handling_fee=handling_fee,
            operation_type=OperationType.BUY if payment_currency != "USDT" else OperationType.SELL
        )
        if payment_currency in ["GCASH", "PAYMAYA"]:
            payment_amount = self._round_to_nearest((Decimal(payment_amount) * Decimal("10000")))
            exchange_amount = self._round_to_nearest((Decimal(payment_amount) / Decimal(price)))
        else:
            exchange_amount = payment_amount
            payment_amount = self._round_to_nearest((Decimal(payment_amount) * Decimal(price)))

        cart = Cart(
            message_id=update.effective_message.message_id,
            language=gina_resp.language,
            group_name=update.effective_chat.title,
            group_id=group_id,
            vendor_name=exchange_rate.group_name,
            vendor_id=exchange_rate.group_id,
            account_name=update.effective_user.username,
            account_id=update.effective_user.id,
            payment_currency=payment_currency,
            payment_amount=float(payment_amount),
            exchange_currency=exchange_currency,
            exchange_amount=float(exchange_amount),
            original_exchange_rate=exchange_rate.buy_rate,
            with_fee_exchange_rate=price,
        )
        cart_id = await self._order_provider.create_cart(cart=cart)
        return messages.CartInfoMessage.format(
            language=gina_resp.language,
            payment_currency=cart.payment_currency,
            exchange_currency=cart.exchange_currency,
            exchange_rate=cart.with_fee_exchange_rate,
            total_price=cart.payment_amount,
            cart_id=cart_id
        )

    @distributed_trace()
    async def on_human_customer_service(self, update: Update, gina_resp: GinaResponse) -> messages.Message:
        """
        on human customer service
        :param update:
        :param gina_resp:
        :return:
        """
        return messages.Message(
            text=await self.format_message(
                message=gina_resp.reply,
                group_id=update.effective_chat.id,
                options=FormatOptions()
            ),
            parse_mode=ParseMode.HTML
        )

    @distributed_trace()
    async def on_get_account(self, update: Update, gina_resp: GinaResponse) -> messages.Message:
        """

        :param update:
        :param gina_resp:
        :return:
        """
        order_info = await self._order_provider.get_order_by_group_id(
            group_id=update.effective_chat.id,
            status=OrderStatus.WAIT_FOR_PAYMENT_ACCOUNT
        )
        if not order_info:
            return messages.OrderInfoNotFoundMessage.format(language=gina_resp.language)
        payload = PaymentAccount(
            order_id=order_info.id,
            customer_id=order_info.group_id,
            vendor_id=order_info.vendor_id,
            payment_currency=order_info.payment_currency,
            exchange_currency=order_info.exchange_currency,
            total_amount=order_info.payment_amount
        )
        await self._vendors_bot_provider.payment_account(payload)
        return messages.Message(text=gina_resp.reply)

    @distributed_trace()
    async def on_confirm_payment(self, update: Update, gina_resp: GinaResponse) -> messages.Message:
        """

        :param update:
        :param gina_resp:
        :return:
        """
        order_info = await self._order_provider.get_order_by_group_id(group_id=update.effective_chat.id)
        if not order_info:
            if order_info.status != OrderStatus.WAIT_FOR_PAYMENT:
                return messages.OrderInfoNotFoundMessage.format(language=gina_resp.language)
        order = Order(
            id=order_info.id,
            status=OrderStatus.WAIT_FOR_CONFIRMATION,
            receive_receipt_at=datetime.now(tz=pytz.UTC)
        )
        await self._order_provider.update_order(order=order)
        payload = ConfirmPayment(
            order_id=order_info.id,
            customer_id=order_info.group_id,
            vendor_id=order_info.vendor_id,
            message_id=order_info.payment_message_id,
        )
        await self._vendors_bot_provider.confirm_payment(payload=payload)
        return messages.Message(text=gina_resp.reply)

    @distributed_trace()
    async def on_payment_check(self, update: Update, gina_resp: GinaResponse) -> messages.Message:
        """

        :param update:
        :param gina_resp:
        :return:
        """
        return messages.Message(text=gina_resp.reply)

    @distributed_trace()
    async def on_cancel_order(self, update: Update, gina_resp: GinaResponse) -> messages.Message:
        """

        :param update:
        :param gina_resp:
        :return:
        """
        order_info = await self._order_provider.get_order_by_group_id(group_id=update.effective_chat.id)
        if not order_info:
            return messages.OrderInfoNotFoundMessage.format(language=gina_resp.language)
        order = Order(
            id=order_info.id,
            status=OrderStatus.CANCELLED,
            done_at=datetime.now(tz=pytz.UTC)
        )
        await self._order_provider.update_order(order=order)
        return messages.Message(text=gina_resp.reply)

    @distributed_trace()
    async def on_hurry(self, update: Update, gina_resp: GinaResponse) -> messages.Message:
        """

        :param update:
        :param gina_resp:
        :return:
        """
        order_info = await self._order_provider.get_order_by_group_id(
            group_id=update.effective_chat.id,
            status=OrderStatus.WAIT_FOR_PAYMENT_ACCOUNT
        )
        if not order_info:
            return messages.OrderInfoNotFoundMessage.format(language=gina_resp.language)
        payload = PaymentAccount(
            order_id=order_info.id,
            customer_id=order_info.group_id,
            vendor_id=order_info.vendor_id,
            payment_currency=order_info.payment_currency,
            exchange_currency=order_info.exchange_currency,
            total_amount=order_info.payment_amount
        )
        await self._vendors_bot_provider.hurry_payment_account(payload=payload)
        return messages.Message(text=gina_resp.reply)

    @distributed_trace()
    async def on_fallback(self, update: Update, gina_resp: GinaResponse) -> messages.Message:
        """
        on fallback
        :param update:
        :param gina_resp:
        :return:
        """
        text = update.message.text
        intent_to_pay = re.compile(r"查收|完成|到|Finish")
        order_info = await self._order_provider.get_order_by_group_id(group_id=update.effective_chat.id)
        if order_info.status == OrderStatus.WAIT_FOR_PAYMENT and intent_to_pay.search(text):
            order = Order(
                id=order_info.id,
                status=OrderStatus.WAIT_FOR_CONFIRMATION,
                receive_receipt_at=datetime.now(tz=pytz.UTC)
            )
            await self._order_provider.update_order(order=order)
            payload = ConfirmPayment(
                order_id=order_info.id,
                customer_id=order_info.group_id,
                vendor_id=order_info.vendor_id,
                message_id=order_info.payment_message_id,
            )
            await self._vendors_bot_provider.confirm_payment(payload=payload)
            return messages.ConfirmPaymentMessage.format(language=order_info.language)
        return messages.Message(text=gina_resp.reply)

    @distributed_trace()
    async def on_exception(self, update: Update, gina_resp: GinaResponse) -> messages.Message:
        """
        on exception
        :param update:
        :param gina_resp:
        :return:
        """
        return messages.Message(text=gina_resp.reply)

    @distributed_trace()
    async def on_order_confirmation(self, update: Update, cart_id: UUID) -> messages.Message:
        """
        order confirmation
        :param update:
        :param cart_id:
        :return:
        """
        cart = await self._order_provider.get_cart_by_id(cart_id=cart_id)
        if not cart:
            return messages.OrderInfoNotFoundMessage.format(language=Language.ZH_TW)
        await self._order_provider.update_cart_status(cart_id=cart.id, status=CartStatus.CONFIRMED)
        order = Order(cart_id=cart.id)
        order_base = await self._order_provider.create_order(order=order)
        payload = PaymentAccount(
            order_id=order_base.id,
            customer_id=cart.group_id,
            vendor_id=cart.vendor_id,
            payment_currency=cart.payment_currency,
            exchange_currency=cart.exchange_currency,
            total_amount=cart.payment_amount
        )
        await self._vendors_bot_provider.payment_account(payload)
        return messages.OrderConfirmationMessage.format(language=cart.language)

    async def format_message(
        self,
        message: str,
        group_id: int,
        options: FormatOptions = None
    ) -> str:
        """
        format message
        :param message:
        :param group_id:
        :param options:
        :return:
        """
        if not options:
            return message
        if options.customer_service:
            message = await self._format_customer_service(message=message, group_id=group_id)
        return message

    async def _format_customer_service(self, message: str, group_id: int) -> str:
        """

        :param message:
        :param group_id:
        :return:
        """
        customer_services = await self._telegram_account_provider.get_group_customer_services(group_id=group_id)
        mention_customer_services = []
        for customer_service in customer_services:
            user = User(
                id=customer_service.id,
                first_name=customer_service.first_name,
                is_bot=customer_service.is_bot,
                last_name=customer_service.last_name,
                username=customer_service.username,
                language_code=customer_service.language_code,
                is_premium=customer_service.is_premium
            )
            mention_customer_services.append(user.mention_html(name=f"@{user.username}"))
        message = message.replace("#CUSTOMER_SERVICE#", " ".join(mention_customer_services))
        return message

    @distributed_trace()
    async def _get_rate_and_fee(
        self,
        group_id: int,
        currency: str,
        operation_type: OperationType
    ) -> tuple[Optional[OptimalExchangeRate], Optional[HandlingFeeConfigItem]]:
        exchange_rate = await self._exchange_rate_provider.get_optimal_exchange_rate(
            currency=currency,
            operation_type=operation_type
        )
        if not exchange_rate:
            return None, None
        handling_fee = await self._handling_fee_provider.get_handling_fee_item_by_group_and_currency(
            group_id=group_id,
            currency_id=exchange_rate.currency_id
        )
        if not handling_fee:
            handling_fee = await self._handling_fee_provider.get_handing_fee_global_item_by_currency(
                currency_id=exchange_rate.currency_id
            )
        return exchange_rate, handling_fee

    @distributed_trace()
    async def _get_price(
        self,
        exchange_rate: OptimalExchangeRate,
        handling_fee: HandlingFeeConfigItem,
        operation_type: OperationType
    ) -> float:
        calculation_type = handling_fee.buy_calculation_type if operation_type == OperationType.BUY else handling_fee.sell_calculation_type
        price = self._calculate_fee(
            calculation_type=calculation_type,
            rate=exchange_rate.buy_rate if operation_type == OperationType.BUY else exchange_rate.sell_rate,
            fee=handling_fee.buy_value if operation_type == OperationType.BUY else handling_fee.sell_value
        )
        return price

    @staticmethod
    def _round_to_nearest(price: Decimal, base: Decimal = Decimal('0.01')) -> Decimal:
        """
        round to the nearest
        :param price:
        :return:
        """
        return (price / base).quantize(Decimal('1'), rounding=ROUND_HALF_UP) * base

    def _calculate_fee(
        self,
        calculation_type: CalculationType,
        rate: float,
        fee: float
    ) -> float:
        """
        calculate fee
        :param rate:
        :param fee:
        :return:
        """
        d_rate, d_fee = Decimal(str(rate)), Decimal(str(fee))
        base = Decimal('0.05')
        match calculation_type:
            case CalculationType.ADDITION:
                result = d_rate + d_fee
            case CalculationType.SUBTRACTION:
                result = d_rate - d_fee
            case CalculationType.MULTIPLICATION:
                result = d_rate * d_fee
            case CalculationType.DIVISION:
                result = d_rate / d_fee
            case _:
                result = d_rate

        round_result = self._round_to_nearest(price=result, base=base)
        return float(round_result)
