"""
TelegramAccountHandler
"""
from starlette import status
from telegram import Bot

from app.exceptions.api_base import APIException
from app.libs.consts.enums import BotType
from app.libs.decorators.sentry_tracer import distributed_trace
from app.providers import TelegramAccountProvider, TelegramGroupTypeProvider
from app.schemas.group_type import GroupTypeRelation
from app.serializers.v1.telegram import (
    TelegramChatGroup,
    TelegramAccount,
    InitGroupMember,
    VendorResponse,
    GroupMembers,
    GroupList,
    GroupPage,
    GroupInfo,
    UpdateGroupInfo,
    GroupQuery,
)


class TelegramAccountHandler:
    """TelegramAccountHandler"""

    def __init__(
        self,
        bot: Bot,
        telegram_account_provider: TelegramAccountProvider,
        group_type_provider: TelegramGroupTypeProvider
    ):
        self._bot = bot
        self._telegram_account_provider = telegram_account_provider
        self._group_type_provider = group_type_provider

    @distributed_trace()
    async def set_account(self, telegram_account: TelegramAccount):
        """
        set account
        :param telegram_account:
        :return:
        """
        await self._telegram_account_provider.set_account(account=telegram_account)

    @distributed_trace()
    async def set_group(self, telegram_group: TelegramChatGroup):
        """
        set group
        :param telegram_group:
        :return:
        """
        await self._telegram_account_provider.set_group(chat_group=telegram_group)

    @distributed_trace()
    async def init_chat_group_member(self, model: InitGroupMember):
        """
        update account group relation
        :param model:
        :return:
        """
        await self._telegram_account_provider.init_chat_group_member(data=model.model_dump())

    @distributed_trace()
    async def delete_chat_group_member(self, account_id: int, group_id: int):
        """
        delete chat group member
        :param account_id:
        :param group_id:
        :return:
        """
        await self._telegram_account_provider.delete_chat_group_member(account_id=account_id, chat_group_id=group_id)

    @distributed_trace()
    async def get_vendors(self) -> VendorResponse:
        """
        get vendors
        :return:
        """
        vendors = await self._telegram_account_provider.get_chat_group_by_bot_type(bot_type=BotType.VENDORS)
        return VendorResponse(vendors=vendors)

    @distributed_trace()
    async def get_chat_groups_by_type(self, group_type: BotType) -> GroupList:
        """
        get chat groups by type
        :param group_type:
        :return:
        """
        groups = await self._telegram_account_provider.get_chat_group_by_bot_type(bot_type=group_type)
        return GroupList(groups=groups)

    @distributed_trace()
    async def get_chat_groups(self, group_query: GroupQuery) -> GroupPage:
        """

        :param group_query:
        :return:
        """
        groups, total = await self._telegram_account_provider.get_chat_groups(query=group_query)
        return GroupPage(
            total=total,
            groups=groups
        )

    @distributed_trace()
    async def get_chat_group(self, group_id: int) -> GroupInfo:
        """
        get chat group
        :param group_id:
        :return:
        """
        group = await self._telegram_account_provider.get_chat_group(group_id=group_id)
        if not group:
            raise APIException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Group Not Found"
            )
        return group

    @distributed_trace()
    async def update_group(self, group_id: int, group_info: UpdateGroupInfo) -> None:
        """
        update chat group
        :param group_id:
        :param group_info:
        :return:
        """
        await self._telegram_account_provider.update_group(group_id=group_id, group_info=group_info)
        if group_info.customer_service_ids:
            await self._telegram_account_provider.update_customer_service(chat_group_id=group_id, is_customer_service=False)
            for customer_service_id in group_info.customer_service_ids:
                await self._telegram_account_provider.update_customer_service(
                    chat_group_id=group_id,
                    account_id=customer_service_id,
                    is_customer_service=True
                )
        if group_info.group_type_ids:
            await self._group_type_provider.delete_group_type_relation(chat_group_id=group_id)
            for group_type_id in group_info.group_type_ids:
                await self._group_type_provider.create_group_type_relation(
                    group_type_relation=GroupTypeRelation(
                        chat_group_id=group_id,
                        chat_group_type_id=group_type_id
                    )
                )

    @distributed_trace()
    async def get_chat_group_members(self, group_id: int) -> GroupMembers:
        """
        get chat group members
        :param group_id:
        :return:
        """
        members = await self._telegram_account_provider.get_chat_group_members(chat_group_id=group_id)
        return GroupMembers(
            total=len(members),
            members=members
        )
