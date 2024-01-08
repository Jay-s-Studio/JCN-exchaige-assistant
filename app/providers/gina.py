"""
GinaProvider
"""
from telegram import Update

from app.clients.gina import GinaClient
from app.models.gina import GinaHeaders, GinaPayload, GinaMessage


class GinaProvider:
    """GinaProvider"""

    def __init__(self):
        self._client = GinaClient()

    async def telegram_messages(self, update: Update):
        """
        telegram messages
        :param update:
        :return:
        """
        headers = GinaHeaders(
            chat_group_id=str(update.effective_chat.id),
            chat_user_id=str(update.effective_user.id),
            chat_platform="telegram",
            chat_mode="group"
        )
        message = GinaMessage(
            text=update.message.text
        )
        payload = GinaPayload(
            messages=[message]
        )
        data = await self._client.messages(headers=headers, payload=payload)
