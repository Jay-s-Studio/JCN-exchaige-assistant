"""
AccountProvider
"""
from typing import Optional

from redis.asyncio import Redis

from app.clients.firebase.firestore import GoogleFirestoreClient
from app.models.account.telegram import TelegramAccount


class TelegramAccountProvider:
    """TelegramAccountProvider"""

    def __init__(self, redis: Redis):
        self._redis = redis
        self.firestore_client = GoogleFirestoreClient()

    @staticmethod
    def redis_name():
        """

        :return:
        """

    async def set_account(self, user_id: str, data: dict) -> Optional[TelegramAccount]:
        """
        set account
        :param user_id:
        :param data:
        :return:
        """
        try:
            await self.firestore_client.set_document(
                collection="account",
                document=user_id,
                data=data
            )
        except Exception as e:
            return None
        return TelegramAccount(**data)

    async def get_account(self, user_id: str) -> Optional[TelegramAccount]:
        """
        get account
        :param user_id:
        :return:
        """
        result = await self.firestore_client.get_document(
            collection="account",
            document=user_id
        )
        if not result.exists:
            return None
        return TelegramAccount(**result.to_dict())

    async def update_chat_group(self, chat_id: str, data: dict):
        """
        update a chat group
        :param chat_id:
        :param data:
        :return:
        """
        result = await self.firestore_client.get_document(
            collection="chat_group",
            document=chat_id
        )
        if result.exists:
            await self.firestore_client.update_document(
                collection="chat_group",
                document=chat_id,
                data=data
            )
            return
        await self.firestore_client.set_document(
            collection="chat_group",
            document=chat_id,
            data=data
        )
