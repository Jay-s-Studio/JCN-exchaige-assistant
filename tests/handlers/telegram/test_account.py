"""
Test account handler.
"""
import pytest

from app.handlers import TelegramAccountHandler
from app.serializers.v1.telegram import UpdateTelegramGroup


@pytest.mark.asyncio
async def test_get_vendors(telegram_account_handler: TelegramAccountHandler):
    """
    Test get_vendors
    :param telegram_account_handler:
    :return:
    """
    vendors = await telegram_account_handler.get_vendors()
    assert vendors is not None
    assert vendors.vendors is not None


@pytest.mark.asyncio
async def test_get_groups(telegram_account_handler: TelegramAccountHandler):
    """
    Test get_groups
    :param telegram_account_handler:
    :return:
    """
    groups = await telegram_account_handler.get_chat_group_by_page()
    assert groups is not None


@pytest.mark.asyncio
async def test_get_group(telegram_account_handler: TelegramAccountHandler):
    """
    Test get_group
    :param telegram_account_handler:
    :return:
    """
    group_id = "-1002050270240"
    group = await telegram_account_handler.get_group(group_id=group_id)
    assert group is not None


@pytest.mark.asyncio
async def test_update_group(telegram_account_handler: TelegramAccountHandler):
    """
    Test update_group
    :param telegram_account_handler:
    :return:
    """
    group_id = "-1002050270240"
    model = UpdateTelegramGroup(
        description="test",
        customer_service_id=1259597115
    )
    await telegram_account_handler.update_group(group_id=group_id, model=model)


@pytest.mark.asyncio
async def test_get_group_members(telegram_account_handler: TelegramAccountHandler):
    """
    Test get_group_members
    :param telegram_account_handler:
    :return:
    """
    group_id = -1002050270240
    group_members = await telegram_account_handler.get_group_members(group_id=group_id)
    assert group_members is not None
