"""
ExchangeRateProvider
"""
from datetime import datetime
from typing import List, Optional

import pytz
import sqlalchemy as sa
from redis.asyncio import Redis

from app.libs.consts.enums import PaymentAccountStatus, OperationType
from app.libs.database import RedisPool, Session
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.logger import logger
from app.schemas.exchange_rate import OptimalExchangeRate
from app.serializers.v1.exchange_rate import GroupExchangeRate, CurrencyIdExRate, CurrencyExRate
from app.models import SysExchangeRate, SysCurrency, SysTelegramChatGroup


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
        try:
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
        except Exception as e:
            raise e
        else:
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
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_exchange_rate(self, group_id: int) -> List[CurrencyIdExRate]:
        """
        Get exchange rate
        :return:
        """
        try:
            result = await (
                self._session.select(
                    SysExchangeRate.currency_id,
                    SysExchangeRate.buy_rate,
                    SysExchangeRate.sell_rate,
                )
                .where(SysExchangeRate.telegram_chat_group_id == group_id)
                .fetch(as_model=CurrencyIdExRate)
            )
        except Exception as e:
            raise e
        else:
            return result
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_optimal_exchange_rate(
        self,
        currency: str,
        operation_type: OperationType
    ) -> Optional[OptimalExchangeRate]:
        """
        Get optimal exchange rate
        :param currency:
        :param operation_type:
        :return:
        """
        if operation_type == OperationType.BUY:
            sa_func = sa.func.min(SysExchangeRate.buy_rate)
        else:
            sa_func = sa.func.max(SysExchangeRate.sell_rate)
        try:
            optimal_exchange_rate = (
                self._session.select(sa_func)
                .select_from(SysExchangeRate)
                .outerjoin(SysCurrency, SysCurrency.id == SysExchangeRate.currency_id)
                .where(SysCurrency.symbol == currency)
                .subquery()
            )

            result = await (
                self._session.select(
                    SysExchangeRate.telegram_chat_group_id.label("group_id"),
                    SysTelegramChatGroup.title.label("group_name"),
                    SysExchangeRate.currency_id,
                    SysCurrency.symbol.label("currency"),
                    SysExchangeRate.buy_rate,
                    SysExchangeRate.sell_rate,
                )
                .outerjoin(SysTelegramChatGroup, SysTelegramChatGroup.id == SysExchangeRate.telegram_chat_group_id)
                .outerjoin(SysCurrency, SysCurrency.id == SysExchangeRate.currency_id)
                .where(SysCurrency.symbol == currency)
                .where(SysExchangeRate.buy_rate == optimal_exchange_rate)
                .where(SysTelegramChatGroup.payment_account_status == PaymentAccountStatus.PREPARING.value)
                .order_by(SysExchangeRate.updated_at.desc())
                .fetchrow(as_model=OptimalExchangeRate)
            )
        except Exception as e:
            raise e
        else:
            return result
        finally:
            await self._session.close()

    @distributed_trace()
    async def batch_update_exchange_rate(self, group_id: int, exchange_rates: List[CurrencyIdExRate]):
        """

        Update exchange rate
        :return:
        """
        await self._session.execute("CREATE TEMP TABLE tmp_exchange_rate  (LIKE public.exchange_rate INCLUDING ALL);")
        try:
            exchange_rate_records = []
            now = datetime.now(tz=pytz.UTC)
            for exchange_rate in exchange_rates:
                exchange_rate_records.append((
                    group_id,
                    exchange_rate.currency_id,
                    exchange_rate.buy_rate,
                    exchange_rate.sell_rate,
                    now,
                    "system",
                    now,
                    "system",
                ))
            await self._session.copy_records_to_table(
                'tmp_exchange_rate',
                records=exchange_rate_records,
                columns=[
                    "telegram_chat_group_id",
                    "currency_id",
                    "buy_rate",
                    "sell_rate",
                    "created_at",
                    "created_by",
                    "updated_at",
                    "updated_by",
                ],
            )
            insert_record = await self._session.execute(
                """
                INSERT INTO public.exchange_rate
                SELECT * FROM tmp_exchange_rate
                ON CONFLICT (telegram_chat_group_id, currency_id) DO UPDATE
                SET buy_rate = EXCLUDED.buy_rate, sell_rate = EXCLUDED.sell_rate, updated_at = now(), updated_by = 'system';
                """
            )
            logger.info(f"Inserted or updated {insert_record} records.")
        except Exception as e:
            await self._session.rollback()
            raise e
        finally:
            await self._session.execute("DROP TABLE IF EXISTS tmp_exchange_rate;")
            await self._session.commit()
            await self._session.close()
