"""
ExchangeRateProvider
"""
from typing import List

from redis.asyncio import Redis

from app.libs.database import RedisPool, Session
from app.libs.decorators.sentry_tracer import distributed_trace
from app.serializers.v1.exchange_rate import GroupExchangeRate
from app.models import SysExchangeRate


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
    async def get_exchange_rate(self, group_id: int):
        """
        Get exchange rate
        :return:
        """

    @distributed_trace()
    async def update_exchange_rate(self, group_id: int, exchange_rate: dict):
        """
        Update exchange rate
        :return:
        """
        data = {
            "telegram_chat_group_id": group_id,
            **exchange_rate
        }
        try:
            await (
                self._session.insert(SysExchangeRate)
                .values(data)
                .on_conflict_do_update(
                    constraint="exchange_rate_telegram_chat_group_id_currency_id_key",
                    set_=data
                )
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()
