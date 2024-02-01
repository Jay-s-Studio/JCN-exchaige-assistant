"""
HandingFeeProvider
"""
from typing import List, Tuple
from uuid import UUID

import sqlalchemy as sa
from redis.asyncio import Redis

from app.libs.database import RedisPool, Session
from app.libs.decorators.sentry_tracer import distributed_trace
from app.models.handing_fee import SysHandingFeeConfig, SysHandingFeeConfigItem
from app.serializers.v1.handing_fee import HandingFeeConfig, HandingFeeConfigItem, HandingFeeConfigBase


class HandingFeeProvider:
    """HandingFeeProvider"""

    def __init__(
        self,
        session: Session,
        redis: RedisPool
    ):
        self._session = session
        self._redis: Redis = redis.create()

    @distributed_trace()
    async def get_handing_fee_config_page(self, page_index: int, page_size: int) -> Tuple[List[HandingFeeConfigBase], int]:
        """
        get handing fee config page
        :param page_index:
        :param page_size:
        :return:
        """
        configs, total = await (
            self._session.select(
                SysHandingFeeConfig.id,
                SysHandingFeeConfig.name,
                SysHandingFeeConfig.is_global,
                SysHandingFeeConfig.description
            )
            .order_by(SysHandingFeeConfig.is_global.desc())
            .limit(page_size)
            .offset(page_index * page_size)
            .fetchpages(as_model=HandingFeeConfigBase)
        )
        return configs, total

    @distributed_trace()
    async def get_handing_fee_config(self, config_id: UUID) -> HandingFeeConfig:
        """
        get handing fee config
        :param config_id:
        :return:
        """
        base_config: HandingFeeConfigBase = await (
            self._session.select(
                SysHandingFeeConfig.id,
                SysHandingFeeConfig.name,
                SysHandingFeeConfig.is_global,
                SysHandingFeeConfig.description
            )
            .where(SysHandingFeeConfig.id == config_id)
            .fetchrow(as_model=HandingFeeConfigBase)
        )
        items = await (
            self._session.select(
                SysHandingFeeConfigItem.currency_id,
                SysHandingFeeConfigItem.buy_calculation_type,
                SysHandingFeeConfigItem.buy_value,
                SysHandingFeeConfigItem.sell_calculation_type,
                SysHandingFeeConfigItem.sell_value
            )
            .where(SysHandingFeeConfigItem.handing_fee_config_id == config_id)
            .fetch(as_model=HandingFeeConfigItem)
        )
        config = HandingFeeConfig(
            **base_config.model_dump(),
            items=items
        )
        return config

    @distributed_trace()
    async def get_global_handing_fee_config(self) -> int:
        """
        get global handing fee config
        :return:
        """
        count = await (
            self._session.select(sa.func.count(SysHandingFeeConfig.id))
            .where(SysHandingFeeConfig.is_global.is_(True))
            .fetchval()
        )
        return count

    @distributed_trace()
    async def create_handing_fee_config(self, config: HandingFeeConfig):
        """
        create handing fee config
        :param config:
        :return:
        """
        data = config.model_dump(exclude={"items"})
        try:
            await (
                self._session.insert(SysHandingFeeConfig)
                .values(data)
                .on_conflict_do_nothing(index_elements=["id"])
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()

    @distributed_trace()
    async def create_handing_fee_config_item(self, config_id: UUID, item: HandingFeeConfigItem):
        """
        create handing fee config item
        :param config_id:
        :param item:
        :return:
        """
        data = item.model_dump()
        data["handing_fee_config_id"] = config_id
        try:
            await (
                self._session.insert(SysHandingFeeConfigItem)
                .values(data)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()

    @distributed_trace()
    async def update_handing_fee_config(self, config_id: UUID, config: HandingFeeConfig):
        """
        update handing fee config
        :param config_id:
        :param config:
        :return:
        """
        data = config.model_dump(exclude={"id", "items"})
        try:
            await (
                self._session.update(SysHandingFeeConfig)
                .where(SysHandingFeeConfig.id == config_id)
                .values(data)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()

    @distributed_trace()
    async def update_handing_fee_config_item(self, config_id: UUID, item: HandingFeeConfigItem):
        """
        update handing fee config item
        :param config_id:
        :param item:
        :return:
        """
        data = item.model_dump()
        data["handing_fee_config_id"] = config_id
        try:
            await (
                self._session.insert(SysHandingFeeConfigItem)
                .values(data)
                .on_conflict_do_update(
                    constraint="unique_handing_fee_config_item_uc",
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
