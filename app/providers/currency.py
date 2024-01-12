"""
CurrencyProvider
"""
import json

from redis.asyncio import Redis

from app.clients.firebase.firestore import GoogleFirestoreClient
from app.libs.database import RedisPool


class CurrencyProvider:
    """CurrencyProvider"""

    def __init__(self, redis: RedisPool):
        self._redis: Redis = redis.create()
        self.firestore_client = GoogleFirestoreClient()
        self.redis_name = "currencies"

    async def get_currencies(self):
        """
        get currencies
        :return:
        """
        if await self._redis.exists(self.redis_name):
            value = await self._redis.get(self.redis_name)
            return json.loads(value)
        result = await self.firestore_client.get_document(
            collection="currency",
            document="currencies"
        )
        if not result.exists:
            return None
        await self._redis.set(self.redis_name, json.dumps(result.to_dict()), ex=60 * 60 * 24)
        return result.to_dict()

    async def update_currencies(self, data: dict):
        """
        update currencies
        :param data:
        :return:
        """
        await self._redis.delete(self.redis_name)
        result = await self.firestore_client.get_document(
            collection="currency",
            document="currencies"
        )
        if result.exists:
            await self.firestore_client.update_document(
                collection="currency",
                document="currencies",
                data=data
            )
            return
        await self.firestore_client.set_document(
            collection="currency",
            document="currencies",
            data=data
        )
