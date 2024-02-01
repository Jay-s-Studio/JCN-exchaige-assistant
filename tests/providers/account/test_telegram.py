"""
Test Telegram provider
"""
import pytest

from app.providers import TelegramAccountProvider


@pytest.mark.asyncio
async def test_get_chat_groups(telegram_account_provider: TelegramAccountProvider):
    """
    Test get_chat_groups
    :param telegram_account_provider:
    :return:
    """
    groups = await telegram_account_provider.get_chat_groups(50, 0)
    assert groups is not None
