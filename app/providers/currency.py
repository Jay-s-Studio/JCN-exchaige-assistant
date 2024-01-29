"""
CurrencyProvider
"""
from typing import List

from redis.asyncio import Redis

from app.libs.database import RedisPool, Session
from app.libs.decorators.sentry_tracer import distributed_trace
from app.models import SysCurrency
from app.schemas.currency import Currency


class CurrencyProvider:
    """CurrencyProvider"""

    def __init__(
        self,
        session: Session,
        redis: RedisPool
    ):
        self._session = session
        self._redis: Redis = redis.create()
        self.redis_name = "currencies"

    @distributed_trace()
    async def get_currencies(self) -> List[Currency]:
        """
        get currencies
        :return:
        """
        try:
            return await self._session.select(SysCurrency).fetch(as_model=Currency)
        except Exception as e:
            raise e
        finally:
            await self._session.close()

    @distributed_trace()
    async def create_currency(self, currency: Currency):
        """
        create currency
        :param currency:
        :return:
        """
        data = currency.model_dump(exclude_none=True)
        try:
            await (
                self._session.insert(SysCurrency)
                .values(**data)
                .on_conflict_do_nothing(index_elements=["id"])
                .execute()
            )
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e
        finally:
            await self._session.close()

    @distributed_trace()
    async def update_currency(self, currency: Currency):
        """
        update currencies
        :param currency:
        :return:
        """
        data = currency.model_dump(
            exclude={"id", "created_at", "created_by"},
            exclude_none=True
        )
        try:
            await (
                self._session.update(SysCurrency)
                .values(**data)
                .where(SysCurrency.id == currency.id)
                .execute()
            )
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e
        finally:
            await self._session.close()
