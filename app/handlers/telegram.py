"""
TelegramHandler
"""
import telegram
from fastapi import HTTPException
from starlette import status
from telegram import Bot

from app.providers import TelegramAccountProvider
from app.serializers.v1.telegram import TelegramBroadcast


class TelegramHandler:
    """TelegramHandler"""

    def __init__(self, bot: Bot, telegram_account_provider: TelegramAccountProvider):
        self._bot = bot
        self._telegram_account_provider = telegram_account_provider

    async def broadcast_message(self, model: TelegramBroadcast):
        """
        broadcast message
        :param model:
        :return:
        """
        group = await self._telegram_account_provider.get_chat_group(chat_id=model.chat_id)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="chat group not found")
        try:
            message = await self._bot.send_message(chat_id=model.chat_id, text=model.message)
        except telegram.error.BadRequest as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return message.to_dict()
