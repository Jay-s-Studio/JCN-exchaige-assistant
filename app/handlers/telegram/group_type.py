"""
TelegramGroupTypeHandler
"""
from uuid import UUID

from app.libs.decorators.sentry_tracer import distributed_trace
from app.providers import TelegramGroupTypeProvider
from app.serializers.v1.telegram.group_type import TelegramGroupType, TelegramGroupTypes


class TelegramGroupTypeHandler:
    """TelegramGroupTypeHandler"""

    def __init__(self, group_type_provider: TelegramGroupTypeProvider):
        self._group_type_provider = group_type_provider

    @distributed_trace()
    async def get_group_types(self) -> TelegramGroupTypes:
        """
        get group types
        :return:
        """
        values = await self._group_type_provider.get_group_types()
        return TelegramGroupTypes(values=values)

    @distributed_trace()
    async def create_group_type(self, group_type: TelegramGroupType) -> UUID:
        """
        create a group type
        :return:
        """
        return await self._group_type_provider.create_group_type(group_type=group_type)

    @distributed_trace()
    async def update_group_type(self, group_type: TelegramGroupType):
        """
        update a group type
        :return:
        """
        return await self._group_type_provider.update_group_type(group_type=group_type)

    @distributed_trace()
    async def delete_group_type(self, group_type_id: UUID):
        """
        delete a group type
        :return:
        """
        return await self._group_type_provider.delete_group_type(group_type_id=group_type_id)
