"""
TelegramAccountHandler
"""
from typing import List, Optional

from starlette import status
from telegram import Bot

from app.exceptions.api_base import APIException
from app.libs.consts.enums import BotType
from app.libs.decorators.sentry_tracer import distributed_trace
from app.schemas.account.telegram import TelegramChatGroup, TelegramAccount
from app.providers import TelegramAccountProvider
from app.serializers.v1.telegram import TelegramGroup, VendorResponse, GroupsResponse, CustomerResponse, GroupMembersResponse, UpdateTelegramGroup


class TelegramAccountHandler:
    """TelegramAccountHandler"""

    def __init__(self, bot: Bot, telegram_account_provider: TelegramAccountProvider):
        self._bot = bot
        self._telegram_account_provider = telegram_account_provider

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
        await self._telegram_account_provider.update_chat_group(chat_group=telegram_group)

    @distributed_trace()
    async def update_account_group_relation(self, account_id: int, group_id: int):
        """
        update account group relation
        :param account_id:
        :param group_id:
        :return:
        """
        await self._telegram_account_provider.update_account_group_relation(account_id=account_id, chat_group_id=group_id)

    @distributed_trace()
    async def delete_chat_group_member(self, account_id: int, group_id: int):
        """
        delete chat group member
        :param account_id:
        :param group_id:
        :return:
        """
        await self._telegram_account_provider.delete_chat_group_member(account_id=account_id, chat_group_id=group_id)

    @staticmethod
    def get_pagination(data: list, page_size: int = 20, page_index: int = 0) -> Optional[list]:
        """

        :param data:
        :param page_size:
        :param page_index:
        :return:
        """
        return data[page_index * page_size: (page_index + 1) * page_size]

    @distributed_trace()
    async def get_chat_group_by_page(
        self,
        page_size: int = 20,
        page_index: int = 0
    ) -> GroupsResponse:
        """

        :param page_size:
        :param page_index:
        :return:
        """
        groups, total = await self._telegram_account_provider.get_chat_group_by_page()
        return GroupsResponse(
            total=total,
            groups=[TelegramGroup(**group.model_dump()) for group in groups]
        )

    @distributed_trace()
    async def get_vendors(self) -> VendorResponse:
        """
        get vendors
        :return:
        """
        vendors = await self._telegram_account_provider.get_chat_group_by_bot_type(bot_type=BotType.VENDORS)
        return VendorResponse(vendors=[TelegramGroup(**vendor.model_dump()) for vendor in vendors])

    @distributed_trace()
    async def get_customers(self) -> CustomerResponse:
        """
        get customers
        :return:
        """
        customers = await self._telegram_account_provider.get_chat_group_by_bot_type(bot_type=BotType.CUSTOMER)
        return CustomerResponse(customers=[TelegramGroup(**customer.model_dump()) for customer in customers])

    @distributed_trace()
    async def get_group(self, group_id: int) -> TelegramGroup:
        """

        :param group_id:
        :return:
        """

    @distributed_trace()
    async def update_group(
        self,
        group_id: str,
        model: UpdateTelegramGroup
    ):
        """

        :param group_id:
        :param model:
        :return:
        """
        pass

    @distributed_trace()
    async def get_group_members(
        self,
        group_id: int,
        page_size: int = 20,
        page_index: int = 0
    ):
        """

        :param group_id:
        :param page_size:
        :param page_index:
        :return:
        """
        members, total = await self._telegram_account_provider.get_chat_group_members(
            chat_id=group_id,
            page_size=page_size,
            page_index=page_index
        )
        return GroupMembersResponse(
            total=total,
            members=members
        )
