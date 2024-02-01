"""
HandlingFeeHandler
"""
from uuid import UUID

from asyncpg import UniqueViolationError
from starlette import status

from app.exceptions.api_base import ResourceExistsException, APIException
from app.libs.decorators.sentry_tracer import distributed_trace
from app.providers import HandlingFeeProvider
from app.serializers.v1.handling_fee import HandlingFeeConfig, HandlingFeeConfigPage


class HandlingFeeHandler:
    """HandlingFeeHandler"""

    def __init__(
        self,
        handling_fee_provider: HandlingFeeProvider,
    ):
        self._handling_fee_provider = handling_fee_provider

    @distributed_trace()
    async def get_handling_fee_config_page(self, page_index: int, page_size: int) -> HandlingFeeConfigPage:
        """
        get handling fee config page
        :param page_index:
        :param page_size:
        :return:
        """
        configs, total = await self._handling_fee_provider.get_handling_fee_config_page(page_index, page_size)
        return HandlingFeeConfigPage(configs=configs, total=total)

    @distributed_trace()
    async def get_handling_fee_config(self, config_id: UUID) -> HandlingFeeConfig:
        """
        get handling fee config
        :param config_id:
        :return:
        """
        config = await self._handling_fee_provider.get_handling_fee_config(config_id)
        return config

    @distributed_trace()
    async def create_handling_fee_config(self, config: HandlingFeeConfig) -> None:
        """
        create handling fee config
        :param config:
        :return:
        """
        try:
            if config.is_global:
                global_config = await self._handling_fee_provider.get_global_handling_fee_config()
                if global_config:
                    raise ResourceExistsException("Global config already exists")
            await self._handling_fee_provider.create_handling_fee_config(config)
            for item in config.items:
                await self._handling_fee_provider.create_handling_fee_config_item(config_id=config.id, item=item)
        except UniqueViolationError:
            raise ResourceExistsException("Config already exists")
        except Exception as e:
            raise APIException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Create handling fee config failed",
                debug_detail=str(e)
            )

    @distributed_trace()
    async def update_handling_fee_config(self, config_id: UUID, config: HandlingFeeConfig) -> None:
        """
        update handling fee config
        :param config_id:
        :param config:
        :return:
        """
        await self._handling_fee_provider.update_handling_fee_config(config_id=config_id, config=config)
        for item in config.items:
            await self._handling_fee_provider.update_handling_fee_config_item(config_id=config_id, item=item)

