"""
ExchangeRateProvider
"""
from typing import List

from redis.asyncio import Redis

from app.libs.database import RedisPool, Session
from app.libs.decorators.sentry_tracer import distributed_trace
from app.serializers.v1.exchange_rate import GroupExchangeRate


class ExchangeRateProvider:
    """ExchangeRateProvider"""

    def __init__(
        self,
        session: Session,
        redis: RedisPool
    ):
        self._session = session
        self._redis: Redis = redis.create()

    @distributed_trace()
    async def get_all_exchange_rate(self) -> List[GroupExchangeRate]:
        """
        Get all exchange rate
        :return:
        """

    @distributed_trace()
    async def get_exchange_rate(self, group_id: str):
        """
        Get exchange rate
        :return:
        """

    @distributed_trace()
    async def update_exchange_rate(self, group_id: str, exchange_rates: dict):
        """
        Update exchange rate
        :return:
        """
