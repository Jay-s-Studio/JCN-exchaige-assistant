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
