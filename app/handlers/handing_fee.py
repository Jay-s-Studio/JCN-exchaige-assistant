"""
HandingFeeHandler
"""
from uuid import UUID

from asyncpg import UniqueViolationError
from starlette import status

from app.exceptions.api_base import ResourceExistsException, ApiBaseException
from app.libs.decorators.sentry_tracer import distributed_trace
from app.providers import HandingFeeProvider
from app.serializers.v1.handing_fee import HandingFeeConfig, HandingFeeConfigPage


class HandingFeeHandler:
    """HandingFeeHandler"""

    def __init__(
        self,
        handing_fee_provider: HandingFeeProvider,
    ):
        self._handing_fee_provider = handing_fee_provider

    @distributed_trace()
    async def get_handing_fee_config_page(self, page_index: int, page_size: int) -> HandingFeeConfigPage:
        """
        get handing fee config page
        :param page_index:
        :param page_size:
        :return:
        """
        configs, total = await self._handing_fee_provider.get_handing_fee_config_page(page_index, page_size)
        return HandingFeeConfigPage(configs=configs, total=total)

    @distributed_trace()
    async def get_handing_fee_config(self, config_id: UUID) -> HandingFeeConfig:
        """
        get handing fee config
        :param config_id:
        :return:
        """
        config = await self._handing_fee_provider.get_handing_fee_config(config_id)
        return config

    @distributed_trace()
    async def create_handing_fee_config(self, config: HandingFeeConfig) -> None:
        """
        create handing fee config
        :param config:
        :return:
        """
        try:
            if config.is_global:
                global_config = await self._handing_fee_provider.get_global_handing_fee_config()
                if global_config:
                    raise ResourceExistsException("Global config already exists")
            await self._handing_fee_provider.create_handing_fee_config(config)
            for item in config.items:
                await self._handing_fee_provider.create_handing_fee_config_item(config_id=config.id, item=item)
        except UniqueViolationError:
            raise ResourceExistsException("Config already exists")
        except Exception as e:
            raise ApiBaseException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Create handing fee config failed",
                debug_detail=str(e)
            )

    @distributed_trace()
    async def update_handing_fee_config(self, config_id: UUID, config: HandingFeeConfig) -> None:
        """
        update handing fee config
        :param config_id:
        :param config:
        :return:
        """
        await self._handing_fee_provider.update_handing_fee_config(config_id=config_id, config=config)
        for item in config.items:
            await self._handing_fee_provider.update_handing_fee_config_item(config_id=config_id, item=item)

