"""
AccountProvider
"""
from redis.asyncio import Redis

from app.clients.firebase.firestore import GoogleFirestoreClient


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

    async def get_account(self, user_id: str):
        """
        get account
        :param user_id:
        :return:
        """
        return await self.firestore_client.get_document(
            collection="account",
            document=user_id
        )
