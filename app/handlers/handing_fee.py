"""
HandingFeeHandler
"""
from app.libs.decorators.sentry_tracer import distributed_trace
from app.providers import HandingFeeProvider
from app.serializers.v1.handing_fee import HandingFee


class HandingFeeHandler:
    """HandingFeeHandler"""

    def __init__(
        self,
        handing_fee_provider: HandingFeeProvider,
    ):
        self._handing_fee_provider = handing_fee_provider

    @distributed_trace()
    async def set_global_handing_fee(self, model: HandingFee):
        """

        :param model:
        :return:
        """
        await self._handing_fee_provider.set_global_handing_fee(
            data=model.model_dump()
        )

    @distributed_trace()
    async def get_global_handing_fee(self) -> HandingFee:
        """

        :return:
        """
        result = await self._handing_fee_provider.get_global_handing_fee()
        if not result:
            return HandingFee()
        return HandingFee(**result)

    @distributed_trace()
    async def update_handing_fee(self, group_id: str, model: HandingFee):
        """

        :param group_id:
        :param model:
        :return:
        """
        await self._handing_fee_provider.update_handing_fee(
            group_id=group_id,
            data=model.model_dump()
        )

    @distributed_trace()
    async def get_handing_fee(self, group_id: str) -> HandingFee:
        """

        :param group_id:
        :return:
        """
        result = await self._handing_fee_provider.get_handing_fee(group_id=group_id)
        if not result:
            return HandingFee()
        return HandingFee(**result)
