"""
HandlingFeeProvider
"""
from typing import List, Tuple, Optional
from uuid import UUID

from redis.asyncio import Redis

from app.libs.database import RedisPool, Session
from app.libs.decorators.sentry_tracer import distributed_trace
from app.models import SysHandlingFeeConfig, SysHandlingFeeConfigItem, SysTelegramChatGroup
from app.serializers.v1.handling_fee import HandlingFeeConfig, HandlingFeeConfigItem, HandlingFeeConfigBase


class HandlingFeeProvider:
    """HandlingFeeProvider"""

    def __init__(
        self,
        session: Session,
        redis: RedisPool
    ):
        self._session = session
        self._redis: Redis = redis.create()

    @distributed_trace()
    async def get_handling_fee_config_page(self, page_index: int, page_size: int) -> Tuple[List[HandlingFeeConfigBase], int]:
        """
        get handling fee config page
        :param page_index:
        :param page_size:
        :return:
        """
        try:
            configs, total = await (
                self._session.select(
                    SysHandlingFeeConfig.id,
                    SysHandlingFeeConfig.name,
                    SysHandlingFeeConfig.is_global,
                    SysHandlingFeeConfig.description
                )
                .order_by(SysHandlingFeeConfig.is_global.desc())
                .limit(page_size)
                .offset(page_index * page_size)
                .fetchpages(as_model=HandlingFeeConfigBase)
            )
        except Exception as e:
            raise e
        else:
            return configs, total
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_handling_fee_config(self, config_id: UUID) -> HandlingFeeConfig:
        """
        get handling fee config
        :param config_id:
        :return:
        """
        try:
            base_config: HandlingFeeConfigBase = await (
                self._session.select(
                    SysHandlingFeeConfig.id,
                    SysHandlingFeeConfig.name,
                    SysHandlingFeeConfig.is_global,
                    SysHandlingFeeConfig.description
                )
                .where(SysHandlingFeeConfig.id == config_id)
                .fetchrow(as_model=HandlingFeeConfigBase)
            )
            items = await (
                self._session.select(
                    SysHandlingFeeConfigItem.currency_id,
                    SysHandlingFeeConfigItem.buy_calculation_type,
                    SysHandlingFeeConfigItem.buy_value,
                    SysHandlingFeeConfigItem.sell_calculation_type,
                    SysHandlingFeeConfigItem.sell_value
                )
                .where(SysHandlingFeeConfigItem.handling_fee_config_id == config_id)
                .fetch(as_model=HandlingFeeConfigItem)
            )
        except Exception as e:
            raise e
        else:
            config = HandlingFeeConfig(
                **base_config.model_dump(),
                items=items
            )
            return config
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_global_handling_fee_config(self) -> Optional[HandlingFeeConfigBase]:
        """
        get global handling fee config
        :return:
        """
        try:
            config = await (
                self._session.select(
                    SysHandlingFeeConfig.id,
                    SysHandlingFeeConfig.name,
                    SysHandlingFeeConfig.is_global,
                    SysHandlingFeeConfig.description
                )
                .where(SysHandlingFeeConfig.is_global.is_(True))
                .fetchrow(as_model=HandlingFeeConfigBase)
            )
        except Exception as e:
            raise e
        else:
            return config
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_handling_fee_item_by_group_and_currency(
        self,
        group_id: int,
        currency_id: UUID
    ) -> Optional[HandlingFeeConfigItem]:
        """
        get handling fee item by group and currency
        :param group_id:
        :param currency_id:
        :return:
        """
        try:
            config = await (
                self._session.select(
                    SysHandlingFeeConfigItem.currency_id,
                    SysHandlingFeeConfigItem.buy_calculation_type,
                    SysHandlingFeeConfigItem.buy_value,
                    SysHandlingFeeConfigItem.sell_calculation_type,
                    SysHandlingFeeConfigItem.sell_value
                )
                .outerjoin(SysTelegramChatGroup, SysTelegramChatGroup.handling_fee_config_id == SysHandlingFeeConfigItem.handling_fee_config_id)
                .where(SysTelegramChatGroup.id == group_id)
                .where(SysHandlingFeeConfigItem.currency_id == currency_id)
                .fetchrow(as_model=HandlingFeeConfigItem)
            )
        except Exception as e:
            raise e
        else:
            return config
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_handing_fee_global_item_by_currency(self, currency_id: UUID) -> Optional[HandlingFeeConfigItem]:
        """
        get handing fee global item by currency
        :param currency_id:
        :return:
        """
        try:
            config = await (
                self._session.select(
                    SysHandlingFeeConfigItem.currency_id,
                    SysHandlingFeeConfigItem.buy_calculation_type,
                    SysHandlingFeeConfigItem.buy_value,
                    SysHandlingFeeConfigItem.sell_calculation_type,
                    SysHandlingFeeConfigItem.sell_value
                )
                .outerjoin(SysHandlingFeeConfig, SysHandlingFeeConfig.id == SysHandlingFeeConfigItem.handling_fee_config_id)
                .where(SysHandlingFeeConfigItem.currency_id == currency_id)
                .where(SysHandlingFeeConfig.is_global.is_(True))
                .fetchrow(as_model=HandlingFeeConfigItem)
            )
        except Exception as e:
            raise e
        else:
            return config
        finally:
            await self._session.close()

    @distributed_trace()
    async def create_handling_fee_config(self, config: HandlingFeeConfig):
        """
        create handling fee config
        :param config:
        :return:
        """
        data = config.model_dump(exclude={"items"})
        try:
            await (
                self._session.insert(SysHandlingFeeConfig)
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
    async def create_handling_fee_config_item(self, config_id: UUID, item: HandlingFeeConfigItem):
        """
        create handling fee config item
        :param config_id:
        :param item:
        :return:
        """
        data = item.model_dump()
        data["handling_fee_config_id"] = config_id
        try:
            await (
                self._session.insert(SysHandlingFeeConfigItem)
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
    async def update_handling_fee_config(self, config_id: UUID, config: HandlingFeeConfig):
        """
        update handling fee config
        :param config_id:
        :param config:
        :return:
        """
        data = config.model_dump(exclude={"id", "items"})
        try:
            await (
                self._session.update(SysHandlingFeeConfig)
                .where(SysHandlingFeeConfig.id == config_id)
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
    async def update_handling_fee_config_item(self, config_id: UUID, item: HandlingFeeConfigItem):
        """
        update handling fee config item
        :param config_id:
        :param item:
        :return:
        """
        data = item.model_dump()
        data["handling_fee_config_id"] = config_id
        try:
            await (
                self._session.insert(SysHandlingFeeConfigItem)
                .values(data)
                .on_conflict_do_update(
                    constraint="unique_handling_fee_config_item_key",
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
