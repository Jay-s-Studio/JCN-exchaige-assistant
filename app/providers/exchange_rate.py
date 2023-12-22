"""
ExchangeRateProvider
"""
import json

from redis.asyncio import Redis

from app.clients.firebase.firestore import GoogleFirestoreClient
from app.libs.database import RedisPool


class ExchangeRateProvider:
    """ExchangeRateProvider"""

    def __init__(self, redis: RedisPool):
        self._redis: Redis = redis.create()
        self.firestore_client = GoogleFirestoreClient()

    async def get_exchange_rate(self, group_id: str):
        """
        Get exchange rate
        :return:
        """
        redis_name = f"exchange_rate:{group_id}"
        if await self._redis.exists(redis_name):
            value = await self._redis.get(redis_name)
            return value
        result = await self.firestore_client.get_document(
            collection="exchange_rate",
            document=group_id
        )
        if not result.exists:
            return None
        await self._redis.set(name=redis_name, value=json.dumps(result.to_dict()), ex=60 * 60 * 6)
        return result.to_dict()

    async def update_exchange_rate(self, group_id: str, currency_rates: dict):
        """
        Update exchange rate
        :return:
        """
        redis_name = f"exchange_rate:{group_id}"
        await self.firestore_client.set_document(
            collection="exchange_rate",
            document=group_id,
            data=currency_rates
        )
        await self._redis.delete(redis_name)