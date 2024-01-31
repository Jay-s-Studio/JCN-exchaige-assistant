"""
ExchangeRateProvider
"""
from typing import List

from redis.asyncio import Redis

from app.libs.database import RedisPool, Session
from app.libs.decorators.sentry_tracer import distributed_trace
from app.serializers.v1.exchange_rate import GroupExchangeRate, CurrencyIdExRate, CurrencyExRate
from app.models import SysExchangeRate, SysCurrency


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
        records = await (
            self._session.select(
                SysExchangeRate.telegram_chat_group_id,
                SysExchangeRate.currency_id,
                SysCurrency.symbol.label("currency"),
                SysExchangeRate.buy_rate,
                SysExchangeRate.sell_rate,
            )
            .outerjoin(SysCurrency, SysCurrency.id == SysExchangeRate.currency_id)
            .fetch()
        )
        group_exchange_rate = {}
        for record in records:
            group_id = record.get("telegram_chat_group_id")
            if group_id not in group_exchange_rate:
                group_exchange_rate[group_id] = []
            group_exchange_rate[group_id].append(CurrencyExRate(**record))
        result = []
        for group_id, exchange_rates in group_exchange_rate.items():
            result.append(GroupExchangeRate(group_id=group_id, exchange_rates=exchange_rates))
        return result

    @distributed_trace()
    async def get_exchange_rate(self, group_id: int) -> List[CurrencyIdExRate]:
        """
        Get exchange rate
        :return:
        """
        result = await (
            self._session.select(
                SysExchangeRate.currency_id,
                SysExchangeRate.buy_rate,
                SysExchangeRate.sell_rate,
            )
            .where(SysExchangeRate.telegram_chat_group_id == group_id)
            .fetch(as_model=CurrencyIdExRate)
        )
        return result

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
