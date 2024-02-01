"""
TelegramMessageHandler
"""
import telegram
from starlette import status
from telegram import Bot

from app.exceptions.api_base import APIException
from app.libs.decorators.sentry_tracer import distributed_trace
from app.providers import TelegramAccountProvider
from app.serializers.v1.telegram import TelegramBroadcast


class TelegramMessageHandler:
    """TelegramMessageHandler"""

    def __init__(self, bot: Bot, telegram_account_provider: TelegramAccountProvider):
        self._bot = bot
        self._telegram_account_provider = telegram_account_provider

    @distributed_trace()
    async def broadcast_message(self, model: TelegramBroadcast):
        """
        broadcast message
        :param model:
        :return:
        """
        # group = await self._telegram_account_provider.get_chat_group(chat_id=model.chat_id)
        # if not group:
        #     raise APIException(status_code=status.HTTP_404_NOT_FOUND, message="chat group not found")
        try:
            message = await self._bot.send_message(chat_id=model.chat_id, text=model.message)
        except telegram.error.BadRequest as e:
            raise APIException(status_code=status.HTTP_400_BAD_REQUEST, message=str(e))
        except Exception as e:
            raise APIException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))
        return message.to_dict()
