"""
TelegramBotMessagesHandler
"""
from telegram import Update

from app.config import settings
from app.context import CustomContext
from app.controllers import MessagesController
from app.libs.database import RedisPool
from app.providers import TelegramAccountProvider
from .base import TelegramBotBaseHandler


class TelegramBotMessagesHandler(TelegramBotBaseHandler):
    """TelegramBotMessagesHandler"""

    def __init__(
        self,
        redis: RedisPool,
        telegram_account_provider: TelegramAccountProvider,
        messages_controller: MessagesController
    ):
        super().__init__(
            redis=redis,
            telegram_account_provider=telegram_account_provider
        )
        self._messages_controller = messages_controller

    @staticmethod
    def redis_name(name: str):
        """

        :return:
        """
        return f"{settings.APP_NAME}:{name}"

    async def receive_message(self, update: Update, context: CustomContext) -> None:
        """
        receive message
        controller
        :param update:
        :param context:
        :return:
        """
        await self.setup_account_info(user=update.effective_user, chat=update.effective_chat)
        await self._messages_controller.receive_message(update=update, context=context)
