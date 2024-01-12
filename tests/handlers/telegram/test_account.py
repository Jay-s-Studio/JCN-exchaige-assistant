"""
Test account handler.
"""
import pytest

from app.handlers import TelegramAccountHandler


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
    assert vendors.total >= 0


@pytest.mark.asyncio
async def test_get_group_members(telegram_account_handler: TelegramAccountHandler):
    """
    Test get_group_members
    :param telegram_account_handler:
    :return:
    """
    group_id = "-1002050270240"
    group_members = await telegram_account_handler.get_group_members(group_id=group_id)
    assert group_members is not None
