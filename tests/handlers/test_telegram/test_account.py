"""
Test account handler.
"""
from uuid import UUID

import pytest

from app.handlers import TelegramAccountHandler
from app.serializers.v1.telegram import UpdateGroupInfo


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
    groups = await telegram_account_handler.get_chat_groups()
    assert groups is not None
    assert groups.groups is not None


@pytest.mark.asyncio
async def test_update_chat_group(telegram_account_handler: TelegramAccountHandler):
    """
    Test update_chat_group
    :param telegram_account_handler:
    :return:
    """
    group_id = -1002050270240
    group = UpdateGroupInfo(
        currency_id=UUID("8d5fb194-2146-4627-a2d7-0561c73ce257"),
        handling_fee_config_id=UUID("73a80953-f74e-431e-8e93-8001e57ad947"),
        group_type_ids=[
            UUID("1c565585-cdc8-4551-9615-5c15d709abca"),
            UUID("ec0563d5-2b10-40a6-95ac-1cd2c9090b8c"),
            UUID("af1caac0-490f-46ca-a758-871a2909ac7f")
        ]
    )
    await telegram_account_handler.update_group(group_id=group_id, group_info=group)
