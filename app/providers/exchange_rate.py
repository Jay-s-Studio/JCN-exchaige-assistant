"""
ExchangeRateProvider
"""
import json
from typing import List

from redis.asyncio import Redis

from app.clients.firebase.firestore import GoogleFirestoreClient
from app.libs.consts.enums import ExpireTime
from app.libs.database import RedisPool
from app.libs.decorators.sentry_tracer import distributed_trace
from app.serializers.v1.exchange_rate import ExchangeRate, GroupExchangeRate


class ExchangeRateProvider:
    """ExchangeRateProvider"""

    def __init__(self, redis: RedisPool):
        self._redis: Redis = redis.create()
        self.firestore_client = GoogleFirestoreClient()

    @distributed_trace()
    async def get_all_exchange_rate(self) -> List[GroupExchangeRate]:
        """
        Get all exchange rate
        :return:
        """
        results = []
        async for document in self.firestore_client.stream(collection="exchange_rate"):
            results.append(GroupExchangeRate(**document.to_dict(), group_id=document.id))
        return results

    @distributed_trace()
    async def get_exchange_rate(self, group_id: str):
        """
        Get exchange rate
        :return:
        """
        redis_name = f"exchange_rate:{group_id}"
        if await self._redis.exists(redis_name):
            value = await self._redis.get(redis_name)
            return json.loads(value)
        result = await self.firestore_client.get_document(
            collection="exchange_rate",
            document=group_id
        )
        if not result.exists:
            return None
        # Cache 6 hours
        await self._redis.set(name=redis_name, value=json.dumps(result.to_dict()), ex=ExpireTime.ONE_HOUR.value * 6)
        return result.to_dict()

    @distributed_trace()
    async def update_exchange_rate(self, group_id: str, exchange_rates: dict):
        """
        Update exchange rate
        :return:
        """
        redis_name = f"exchange_rate:{group_id}"
        result = await self.firestore_client.get_document(
            collection="exchange_rate",
            document=group_id
        )
        if result.exists:
            await self.firestore_client.update_document(
                collection="exchange_rate",
                document=group_id,
                data=exchange_rates
            )
            await self._redis.delete(redis_name)
            return
        await self.firestore_client.set_document(
            collection="exchange_rate",
            document=group_id,
            data=exchange_rates
        )
        await self._redis.delete(redis_name)
