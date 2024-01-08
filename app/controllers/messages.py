"""
MessagesController
"""
import asyncio

from telegram import Update

from app.context import CustomContext
from app.providers import GinaProvider


class MessagesController:
    """MessagesController"""

    def __init__(self, gina_provider: GinaProvider):
        self._gina_provider = gina_provider

    async def receive_message(self, update: Update, context: CustomContext) -> None:
        """
        receive message
        :param update:
        :param context:
        :return:
        """
        await update.effective_chat.send_chat_action("typing")
        await asyncio.sleep(10)
        await update.effective_message.reply_text(text="Hello World")
        # result = await self._gina_provider.telegram_messages(update=update)

