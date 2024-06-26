"""
TelegramMessageHandler
"""
import traceback
from datetime import datetime, timedelta
from decimal import Decimal

import pytz
import telegram
from httpx import HTTPStatusError
from starlette import status
from telegram import Bot

from app.exceptions.api_base import APIException
from app.libs.consts.enums import OrderStatus, BotType, MessageStatus, OperationType
from app.libs.consts.messages import ConfirmPayMessage
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.logger import logger
from app.libs.utils.calculator import Calculator
from app.providers import TelegramAccountProvider, OrderProvider, MessageProvider, VendorsBotProvider, ExchangeRateProvider, PriceProvider
from app.schemas.broadcast_message import BroadcastMessage, BroadcastMessageHistory
from app.schemas.order import Order
from app.schemas.vendors_bot import VendorBotBroadcast, GetPaymentAccount
from app.serializers.v1.telegram import (
    TelegramBroadcast,
    PaymentAccount,
    GroupPaymentAccountStatus,
    ConfirmPay,
    OrderPaymentAccountStatus,
)


class TelegramMessageHandler:
    """TelegramMessageHandler"""

    def __init__(
        self,
        bot: Bot,
        telegram_account_provider: TelegramAccountProvider,
        order_provider: OrderProvider,
        price_provider: PriceProvider,
        message_provider: MessageProvider,
        vendors_bot_provider: VendorsBotProvider
    ):
        self._bot = bot
        self._telegram_account_provider = telegram_account_provider
        self._order_provider = order_provider
        self._price_provider = price_provider
        self._message_provider = message_provider
        self._vendors_bot_provider = vendors_bot_provider

    @distributed_trace()
    async def broadcast_message(self, model: TelegramBroadcast):
        """
        broadcast message
        :param model:
        :return:
        """
        message = BroadcastMessage(content=model.message, type=model.type)
        broadcast_message_id = await self._message_provider.create_message(message=message)
        for chat_id in model.chat_id_list:
            history = BroadcastMessageHistory(message_id=broadcast_message_id, chat_group_id=chat_id)
            await self._message_provider.create_message_history(message_history=history)
            try:
                match model.type:
                    case BotType.CUSTOMER:
                        resp = await self._bot.send_message(chat_id=chat_id, text=model.message)
                        history.telegram_message_id = resp.message_id
                    case BotType.VENDORS:
                        payload = VendorBotBroadcast(chat_id=chat_id, message=model.message)
                        resp = await self._vendors_bot_provider.broadcast(payload=payload)
                        history.telegram_message_id = resp.message_id
            except telegram.error.BadRequest as exc:
                history.status = MessageStatus.FAILED
                history.telegram_error_description = exc.message
            except HTTPStatusError as exc:
                history.status = MessageStatus.FAILED
                history.telegram_error_description = f"({exc.response.status_code}) {exc.response.text}"
            except Exception as exc:
                history.status = MessageStatus.FAILED
                history.telegram_error_description = traceback.format_exc()
                logger.error(exc)
            else:
                history.status = MessageStatus.SENT
            finally:
                await self._message_provider.update_message_history(message_history=history)

    @distributed_trace()
    async def receive_payment_account(self, model: PaymentAccount):
        """
        receive payment account
        :param model:
        :return:
        """
        now = datetime.now(tz=pytz.UTC)
        order_info = await self._order_provider.get_order_by_id(order_id=model.order_id)
        if not order_info:
            raise APIException(status_code=status.HTTP_404_NOT_FOUND, message="order not found")
        try:
            message = await self._bot.send_message(
                chat_id=order_info.group_id,
                text=model.message,
                reply_to_message_id=order_info.message_id
            )
            order = Order(
                id=order_info.id,
                expiration_of_pay=now + timedelta(hours=1),
                payment_account=model.message,
                payment_message_id=model.message_id,
                receive_payment_account_at=now,
                status=OrderStatus.WAIT_FOR_PAYMENT
            )
            await self._order_provider.update_order(order=order)
        except telegram.error.BadRequest as e:
            raise APIException(status_code=status.HTTP_400_BAD_REQUEST, message=str(e))
        except Exception as e:
            raise APIException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))
        return message.to_dict()

    @distributed_trace()
    async def update_payment_account_status(
        self,
        group_id: int,
        model: GroupPaymentAccountStatus
    ) -> None:
        """
        update group payment account status
        :param group_id:
        :param model:
        :return:
        """
        await self._telegram_account_provider.update_payment_account_status(
            group_id=group_id,
            status=model.status
        )

    @distributed_trace()
    async def order_payment_account_status(
        self,
        group_id: int,
        model: OrderPaymentAccountStatus
    ) -> None:
        """
        update group payment account status
        :param group_id:
        :param model:
        :return:
        """
        await self._telegram_account_provider.update_payment_account_status(
            group_id=group_id,
            status=model.status
        )
        order = await self._order_provider.get_order_by_id(order_id=model.order_id)
        cart = await self._order_provider.get_cart_by_id(cart_id=order.cart_id)
        price_info = await self._price_provider.get_price_info(
            group_id=order.group_id,
            currency=order.payment_currency if order.payment_currency != "USDT" else order.exchange_currency,
            operation_type=OperationType.BUY if order.payment_currency != "USDT" else OperationType.SELL
        )
        cart.vendor_name = price_info.vendor_name
        cart.vendor_id = price_info.vendor_id
        cart.exchange_amount = Calculator.round_to_nearest((Decimal(cart.payment_amount) / Decimal(price_info.price)))
        cart.original_exchange_rate = price_info.original_rate
        cart.price = price_info.price
        await self._order_provider.update_cart(cart=cart)
        payload = GetPaymentAccount(
            order_id=order.id,
            customer_id=cart.group_id,
            vendor_id=cart.vendor_id,
            payment_currency=cart.payment_currency,
            exchange_currency=cart.exchange_currency,
            total_amount=cart.payment_amount
        )
        await self._vendors_bot_provider.payment_account(payload)

    @distributed_trace()
    async def confirm_pay(self, model: ConfirmPay):
        """
        confirm pay
        :param model:
        :return:
        """
        order_info = await self._order_provider.get_order_by_id(order_id=model.order_id)
        if not order_info:
            raise APIException(status_code=status.HTTP_404_NOT_FOUND, message="order not found")
        cart_info = await self._order_provider.get_cart_by_id(cart_id=order_info.cart_id)
        message = ConfirmPayMessage.format(language=cart_info.language)
        try:
            resp_message = await self._bot.send_message(
                chat_id=order_info.group_id,
                text=message.text,
                parse_mode=message.parse_mode,
                reply_to_message_id=order_info.message_id
            )
            order = Order(
                id=order_info.id,
                status=OrderStatus.DONE,
                done_at=datetime.now(tz=pytz.UTC)
            )
            await self._order_provider.update_order(order=order)
        except telegram.error.BadRequest as e:
            raise APIException(status_code=status.HTTP_400_BAD_REQUEST, message=str(e))
        except Exception as e:
            raise APIException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))
        return resp_message.to_dict()
