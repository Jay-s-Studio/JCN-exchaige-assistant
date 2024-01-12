"""
TelegramAccountHandler
"""
from typing import List, Optional

from starlette import status
from telegram import Bot

from app.exceptions.api_base import APIException
from app.libs.consts.enums import BotType
from app.models.account.telegram import TelegramChatGroup, TelegramAccount
from app.providers import TelegramAccountProvider
from app.serializers.v1.telegram import TelegramGroup, VendorResponse, GroupsResponse, CustomerResponse, GroupMembersResponse, UpdateCustomerService


class TelegramAccountHandler:
    """TelegramAccountHandler"""

    def __init__(self, bot: Bot, telegram_account_provider: TelegramAccountProvider):
        self._bot = bot
        self._telegram_account_provider = telegram_account_provider

    @staticmethod
    def get_pagination(data: list, page_size: int = 20, page_index: int = 0) -> Optional[list]:
        """

        :param data:
        :param page_size:
        :param page_index:
        :return:
        """
        return data[page_index * page_size: (page_index + 1) * page_size]

    async def get_groups(self, page_size: int = 20, page_index: int = 0):
        """

        :param page_size:
        :param page_index:
        :return:
        """
        accounts = await self._telegram_account_provider.get_all_chat_group()
        total = len(accounts)
        if not accounts:
            return
        if page_index * page_size > total:
            return
        page_of_groups: List[TelegramChatGroup] = self.get_pagination(data=accounts, page_size=page_size, page_index=page_index)
        groups = [
            TelegramGroup(
                id=value.id,
                title=value.title,
                description=value.custom_info.description,
                has_bot=value.custom_info.in_group,
                bot_type=value.custom_info.bot_type,
                customer_service=value.custom_info.customer_service
            ) for value in page_of_groups
        ]
        return GroupsResponse(
            total=total,
            groups=groups
        )

    async def get_vendors(self, page_size: int = 20, page_index: int = 0) -> VendorResponse:
        """
        get vendors
        :param page_size:
        :param page_index:
        :return:
        """
        accounts = await self._telegram_account_provider.get_all_chat_group()
        vendors_list: List[TelegramChatGroup] = list(
            filter(
                lambda x: x.custom_info.bot_type == BotType.VENDORS if x.custom_info else False, accounts
            )
        )
        total = len(vendors_list)
        if not vendors_list:
            return VendorResponse()
        if page_index * page_size > total:
            return VendorResponse(total=total)
        page_of_vendors: List[TelegramChatGroup] = self.get_pagination(data=vendors_list, page_size=page_size, page_index=page_index)
        vendors = [
            TelegramGroup(
                id=value.id,
                title=value.title,
                description=value.custom_info.description,
                has_bot=value.custom_info.in_group,
                bot_type=value.custom_info.bot_type
            ) for value in page_of_vendors
        ]
        return VendorResponse(
            total=total,
            vendors=vendors
        )

    async def get_customers(self, page_size: int = 20, page_index: int = 0) -> CustomerResponse:
        """
        get customers
        :param page_size:
        :param page_index:
        :return:
        """
        accounts = await self._telegram_account_provider.get_all_chat_group()
        customers_list: List[TelegramChatGroup] = list(
            filter(
                lambda x: x.custom_info.bot_type == BotType.CUSTOMER if x.custom_info else False, accounts
            )
        )
        total = len(customers_list)
        if not customers_list:
            return CustomerResponse()
        if page_index * page_size > total:
            return CustomerResponse(total=total)
        page_of_customers: List[TelegramChatGroup] = self.get_pagination(data=customers_list, page_size=page_size, page_index=page_index)
        customers = [
            TelegramGroup(
                id=value.id,
                title=value.title,
                description=value.custom_info.description,
                has_bot=value.custom_info.in_group,
                bot_type=value.custom_info.bot_type,
                customer_service=value.custom_info.customer_service
            ) for value in page_of_customers
        ]
        return CustomerResponse(
            total=total,
            customers=customers
        )

    async def get_group_members(
        self,
        group_id: str,
        page_size: int = 20,
        page_index: int = 0
    ):
        """

        :param group_id:
        :param page_size:
        :param page_index:
        :return:
        """
        accounts = await self._telegram_account_provider.get_chat_group_members(chat_id=group_id)
        total = len(accounts)
        if not accounts:
            return
        if page_index * page_size > total:
            return
        members: List[TelegramAccount] = self.get_pagination(data=accounts, page_size=page_size, page_index=page_index)
        return GroupMembersResponse(
            total=total,
            members=members
        )

    # async def update_group_customer_service(
    #     self,
    #     model: UpdateCustomerService
    # ):
    #     """
    #
    #     :param model:
    #     :return:
    #     """
    #     customer_service = await self._telegram_account_provider.get_account(user_id=model.customer_service_id)
    #     if not customer_service:
    #         raise APIException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             message="Account Not Found"
    #         )
    #     result = await self._telegram_account_provider.update_group_customer_service(
    #         chat_id=model.group_id,
    #         customer_service=customer_service
    #     )
    #     if not result:
    #         raise APIException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             message="Group Not Found"
    #         )
