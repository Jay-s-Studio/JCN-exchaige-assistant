"""
Test Telegram provider
"""
from uuid import UUID

import pytest

from app.libs.consts.enums import PaymentAccountStatus
from app.providers import TelegramAccountProvider
from app.serializers.v1.telegram import UpdateGroupInfo, GroupQuery

UPDATE_GROUP_INFO = UpdateGroupInfo(
    description="Test description",
    customer_service_ids=[1259597115],
    currency_id=UUID("5589c1fe-353b-4684-8b46-7580c9046c55"),
    handling_fee_config_id=UUID("87e3e18b-2dd2-45e6-9c15-4d6b493abae6")
)


@pytest.mark.asyncio
async def test_get_chat_groups(telegram_account_provider: TelegramAccountProvider):
    """
    Test get_chat_groups
    :param telegram_account_provider:
    :return:
    """
    query = GroupQuery()
    groups = await telegram_account_provider.get_chat_groups(query=query)
    assert groups is not None


@pytest.mark.asyncio
async def test_get_chat_group(telegram_account_provider: TelegramAccountProvider):
    """
    Test get_chat_group
    :param telegram_account_provider:
    :return:
    """
    group = await telegram_account_provider.get_chat_group(-1002050270240)
    assert group is not None


@pytest.mark.asyncio
async def test_update_group(telegram_account_provider: TelegramAccountProvider):
    """
    Test update_group
    :param telegram_account_provider:
    :return:
    """
    update_group_info = UPDATE_GROUP_INFO
    await telegram_account_provider.update_group(group_id=-1002050270240, group_info=update_group_info)


@pytest.mark.asyncio
async def test_update_customer_service(telegram_account_provider: TelegramAccountProvider):
    """
    Test update_customer_service
    :param telegram_account_provider:
    :return:
    """
    await telegram_account_provider.update_customer_service(
        chat_group_id=-1002050270240,
        account_id=1259597115,
        is_customer_service=True
    )


@pytest.mark.asyncio
async def test_get_chat_group_members(telegram_account_provider: TelegramAccountProvider):
    """
    Test get_chat_group_members
    :param telegram_account_provider:
    :return:
    """
    members = await telegram_account_provider.get_chat_group_members(chat_group_id=-1002050270240)
    assert members is not None


@pytest.mark.asyncio
async def test_get_group_customer_services(telegram_account_provider: TelegramAccountProvider):
    """
    Test get_group_customer_services
    :param telegram_account_provider:
    :return:
    """
    customer_services = await telegram_account_provider.get_group_customer_services(group_id=-1002050270240)
    assert customer_services is not None


@pytest.mark.asyncio
async def test_update_group_payment_account_status(telegram_account_provider: TelegramAccountProvider):
    """
    Test update_group_payment_account_status
    :param telegram_account_provider:
    :return:
    """
    await telegram_account_provider.update_payment_account_status(
        group_id=-1002003483337,
        status=PaymentAccountStatus.PREPARING
    )
