"""
TelegramMessageHandler
"""
from datetime import datetime, timedelta

import pytz
import telegram
from starlette import status
from telegram import Bot

from app.exceptions.api_base import APIException
from app.libs.consts.enums import OrderStatus, BotType, MessageStatus
from app.libs.consts.messages import ConfirmPayMessage
from app.libs.decorators.sentry_tracer import distributed_trace
from app.providers import TelegramAccountProvider, OrderProvider, MessageProvider
from app.schemas.broadcast_message import BroadcastMessage, BroadcastMessageHistory
from app.schemas.order import Order
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
        message_provider: MessageProvider
    ):
        self._bot = bot
        self._telegram_account_provider = telegram_account_provider
        self._order_provider = order_provider
        self._message_provider = message_provider

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
                        # call vendor bot api
                        pass
            except telegram.error.BadRequest as e:
                history.status = MessageStatus.FAILED
                history.telegram_error_description = e.message
            except Exception as e:
                history.status = MessageStatus.FAILED
                history.telegram_error_description = str(e)
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
        # TODO: Get order info and second lowest price

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
