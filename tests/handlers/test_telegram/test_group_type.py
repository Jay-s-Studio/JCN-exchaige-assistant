"""
Test group type handler.
"""
from uuid import UUID

import pytest

from app.handlers import TelegramGroupTypeHandler
from app.serializers.v1.telegram import TelegramGroupType, TelegramGroupTypes


@pytest.mark.asyncio
async def test_get_group_types(telegram_group_type_handler: TelegramGroupTypeHandler):
    """
    Test get_group_types
    :param telegram_group_type_handler:
    :return:
    """
    result = await telegram_group_type_handler.get_group_types()
    assert isinstance(result, TelegramGroupTypes)


@pytest.mark.asyncio
async def test_create_group_type(telegram_group_type_handler: TelegramGroupTypeHandler):
    """
    Test create_group_type
    :param telegram_group_type_handler:
    :return:
    """
    group_type = TelegramGroupType(
        name="PHP Customer",
    )
    result = await telegram_group_type_handler.create_group_type(group_type=group_type)
    assert isinstance(result, UUID)


@pytest.mark.asyncio
async def test_update_group_type(telegram_group_type_handler: TelegramGroupTypeHandler):
    """
    Test update_group_type
    :param telegram_group_type_handler:
    :return:
    """
    group_type = TelegramGroupType(
        id=UUID("ed8a0d0a-e555-4a95-b19e-4b384ec5888c"),
        name="PHP Customer 123",
    )
    result = await telegram_group_type_handler.update_group_type(group_type=group_type)
    assert result is None
