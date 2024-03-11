"""
MessagesController
"""
import asyncio
import uuid
from dataclasses import dataclass
from typing import Optional

from telegram import Update, User
from telegram.constants import ParseMode

from app.libs.consts import messages
from app.libs.consts.enums import GinaAction, CurrencySymbol, OperationType, CalculationType, OrderStatus
from app.libs.consts.messages import Message, OrderInfoNotFoundMessage, OrderInProgressMessage
from app.libs.decorators.sentry_tracer import distributed_trace
from app.providers import ExchangeRateProvider, TelegramAccountProvider, HandlingFeeProvider, OrderProvider, VendorsBotProvider
from app.schemas.exchange_rate import OptimalExchangeRate
from app.schemas.files import TelegramFile
from app.schemas.gina import GinaResponse
from app.schemas.order import Order
from app.schemas.vendors_bot import PaymentAccount, CheckReceipt
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
    async def on_exchange_rate(self, update: Update, gina_resp: GinaResponse) -> Message:
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
                message = Message(text=gina_resp.reply)
        return message

    @distributed_trace()
    async def _exchange_rate(self, update: Update, gina_resp: GinaResponse, get_default: bool = False) -> Message:
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
    async def on_swap(self, update: Update, gina_resp: GinaResponse) -> Message:
        """
        on swap
        :param update:
        :param gina_resp:
        :return:
        """
        # order_info = await self._order_provider.get_order_by_group_id(group_id=update.effective_chat.id)
        # if order_info:
        #     if order_info.status not in [OrderStatus.EXPIRE, OrderStatus.PAID, OrderStatus.CANCELLED]:
        #         return OrderInProgressMessage.format(language=gina_resp.language)
        match gina_resp.action:
            case GinaAction.SWAP:
                message = await self._swap(update=update, gina_resp=gina_resp)
            case GinaAction.SWAP_CRYPTO:
                message = await self._swap(update=update, gina_resp=gina_resp)
            case GinaAction.SWAP_LEGAL:
                message = Message(text=gina_resp.reply)
            case _:
                message = Message(text=gina_resp.reply)
        return message

    @distributed_trace()
    async def _swap(self, update: Update, gina_resp: GinaResponse) -> Message:
        """
        swap
        :param update:
        :param gina_resp:
        :return:
        """
        session_id = uuid.uuid4()
        group_id = update.effective_chat.id
        payment_currency = gina_resp.payment_currency
        exchange_currency = gina_resp.exchange_currency
        currency = payment_currency
        if exchange_currency == "G":
            exchange_currency = "GCASH"
            currency = exchange_currency
        if exchange_currency == "M":
            exchange_currency = "PAYMAYA"
            currency = exchange_currency
        if exchange_currency != "USDT":
            currency = exchange_currency

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
        # order_cache = OrderCache(
        #     session_id=session_id,
        #     language=gina_resp.language,
        #     message_id=update.effective_message.message_id,
        #     group_id=group_id,
        #     amount_to_exchange=gina_resp.amount_to_exchange,
        #     payment_currency=payment_currency,
        #     exchange_currency=exchange_currency,
        #     vendor_id=exchange_rate.group_id,
        #     original_exchange_rate=exchange_rate.buy_rate,
        #     with_fee_exchange_rate=price,
        #     total_amount=price * gina_resp.amount_to_exchange
        # )
        # await self._order_provider.create_order(
        #     group_id=group_id,
        #     order_id=session_id,
        #     order_info=order_cache
        # )
        payload = PaymentAccount(
            session_id=session_id,
            customer_id=group_id,
            group_id=exchange_rate.group_id,
            payment_currency=payment_currency,
            exchange_currency=exchange_currency,
            total_amount=price * gina_resp.amount_to_exchange
        )
        await self._vendors_bot_provider.payment_account(payload)
        return Message(text=gina_resp.reply)

    @distributed_trace()
    async def on_human_customer_service(self, update: Update, gina_resp: GinaResponse) -> Message:
        """
        on human customer service
        :param update:
        :param gina_resp:
        :return:
        """
        return Message(
            text=await self.format_message(
                message=gina_resp.reply,
                group_id=update.effective_chat.id,
                options=FormatOptions()
            ),
            parse_mode=ParseMode.HTML
        )

    @distributed_trace()
    async def on_get_account(self, update: Update, gina_resp: GinaResponse) -> Message:
        """

        :param update:
        :param gina_resp:
        :return:
        """
        # order_info = await self._order_provider.get_order_by_group_id(group_id=update.effective_chat.id)
        # if not order_info:
        #     return OrderInfoNotFoundMessage.format(language=gina_resp.language)
        # payload = PaymentAccount(
        #     session_id=order_info.session_id,
        #     customer_id=order_info.group_id,
        #     group_id=order_info.vendor_id,
        #     payment_currency=order_info.payment_currency,
        #     exchange_currency=order_info.exchange_currency,
        #     total_amount=order_info.total_amount
        # )
        # await self._vendors_bot_provider.payment_account(payload)
        return Message(text=gina_resp.reply)

    @distributed_trace()
    async def on_receipt(self, update: Update, gina_resp: GinaResponse, telegram_file: TelegramFile) -> Message:
        """

        :param update:
        :param gina_resp:
        :param telegram_file:
        :return:
        """
        # order_info = await self._order_provider.get_order_by_group_id(group_id=update.effective_chat.id)
        # if not order_info:
        #     return OrderInfoNotFoundMessage.format(language=gina_resp.language)
        # payload = CheckReceipt(
        #     session_id=order_info.session_id,
        #     customer_id=order_info.group_id,
        #     group_id=order_info.vendor_id,
        #     file_id=telegram_file.file_unique_id,
        #     file_name=telegram_file.file_name
        # )
        # await self._vendors_bot_provider.check_receipt(payload=payload)
        # order_info.status = OrderStatus.WAIT_FOR_CONFIRMATION
        # await self._order_provider.update_order(
        #     group_id=update.effective_chat.id,
        #     order_id=order_info.session_id,
        #     order_info=order_info
        # )
        return Message(text=gina_resp.reply)

    @distributed_trace()
    async def on_payment_check(self, update: Update, gina_resp: GinaResponse) -> Message:
        """

        :param update:
        :param gina_resp:
        :return:
        """
        return Message(text=gina_resp.reply)

    @distributed_trace()
    async def on_cancel_order(self, update: Update, gina_resp: GinaResponse) -> Message:
        """

        :param update:
        :param gina_resp:
        :return:
        """
        # order_info = await self._order_provider.get_order_by_group_id(group_id=update.effective_chat.id)
        # if not order_info:
        #     return OrderInfoNotFoundMessage.format(language=gina_resp.language)
        # order_info.status = OrderStatus.CANCELLED
        # await self._order_provider.update_order(
        #     group_id=update.effective_chat.id,
        #     order_id=order_info.session_id,
        #     order_info=order_info
        # )
        return Message(text=gina_resp.reply)

    @distributed_trace()
    async def on_hurry(self, update: Update, gina_resp: GinaResponse) -> Message:
        """

        :param update:
        :param gina_resp:
        :return:
        """
        # order_info = await self._order_provider.get_order_by_group_id(group_id=update.effective_chat.id)
        # if not order_info:
        #     return OrderInfoNotFoundMessage.format(language=gina_resp.language)
        # payload = PaymentAccount(
        #     session_id=order_info.session_id,
        #     customer_id=order_info.group_id,
        #     group_id=order_info.vendor_id,
        #     payment_currency=order_info.payment_currency,
        #     exchange_currency=order_info.exchange_currency,
        #     total_amount=order_info.total_amount
        # )
        # await self._vendors_bot_provider.hurry_payment_account(payload=payload)
        return Message(text=gina_resp.reply)

    @distributed_trace()
    async def on_fallback(self, update: Update, gina_resp: GinaResponse) -> Message:
        """
        on fallback
        :param update:
        :param gina_resp:
        :return:
        """
        return Message(text=gina_resp.reply)

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
    def _calculate_fee(
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
        match calculation_type:
            case CalculationType.ADDITION:
                return rate + fee
            case CalculationType.SUBTRACTION:
                return rate - fee
            case CalculationType.MULTIPLICATION:
                return rate * fee
            case CalculationType.DIVISION:
                return rate / fee
            case _:
                return rate
