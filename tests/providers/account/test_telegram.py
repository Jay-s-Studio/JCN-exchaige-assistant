"""
Test Telegram provider
"""
import pytest

from app.providers import TelegramAccountProvider


@pytest.mark.asyncio
async def test_get_chat_group(telegram_account_provider: TelegramAccountProvider):
    """
    Test get chat group
    :param telegram_account_provider:
    :return:
    """
    group = await telegram_account_provider.get_chat_group(chat_id=-1002050270240)
    assert group
    assert group.id == -1002050270240


@pytest.mark.asyncio
async def test_get_chat_group_members(telegram_account_provider: TelegramAccountProvider):
    """
    Test get group members
    :param telegram_account_provider:
    :return:
    """
    members = await telegram_account_provider.get_all_chat_group_members(
        chat_id=-1002050270240
    )
    assert members
    assert len(members) > 0
