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


@pytest.mark.asyncio
async def test_get_chat_groups(telegram_account_handler: TelegramAccountHandler):
    """
    Test get_chat_groups
    :param telegram_account_handler:
    :return:
    """
    groups = await telegram_account_handler.get_chat_groups(50, 0)
    assert groups is not None
    assert groups.groups is not None
