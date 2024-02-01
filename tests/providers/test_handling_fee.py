"""
Test handling fee provider
"""
from uuid import UUID

import pytest

from app.libs.consts.enums import CalculationType, OperationType
from app.providers import HandlingFeeProvider
from app.serializers.v1.handling_fee import HandlingFeeConfig, HandlingFeeConfigItem


@pytest.mark.asyncio
async def test_get_handling_fee_config_page(
    handling_fee_provider: HandlingFeeProvider
):
    """
    Test get handling fee config page
    """
    config, total = await handling_fee_provider.get_handling_fee_config_page(0, 10)
    assert config, total


@pytest.mark.asyncio
async def test_get_handling_fee_config(
    handling_fee_provider: HandlingFeeProvider
):
    """
    Test get handling fee config
    """
    config = await handling_fee_provider.get_handling_fee_config(UUID("87e3e18b-2dd2-45e6-9c15-4d6b493abae6"))
    assert config


@pytest.mark.asyncio
async def test_get_global_handling_fee_config(
    handling_fee_provider: HandlingFeeProvider
):
    """
    Test get global handling fee config
    """
    config = await handling_fee_provider.get_global_handling_fee_config()
    assert config <= 1


@pytest.mark.asyncio
async def test_create_handling_fee_config(
    handling_fee_provider: HandlingFeeProvider
):
    """
    Test create handling fee config
    """
    config = HandlingFeeConfig(
        id=UUID("87e3e18b-2dd2-45e6-9c15-4d6b493abae6"),
        name="Test",
        items=[]
    )
    await handling_fee_provider.create_handling_fee_config(config)


@pytest.mark.asyncio
async def test_create_handling_fee_config_item(
    handling_fee_provider: HandlingFeeProvider
):
    """
    Test create handling fee config item
    """
    await handling_fee_provider.create_handling_fee_config_item(
        config_id=UUID("87e3e18b-2dd2-45e6-9c15-4d6b493abae6"),
        item=HandlingFeeConfigItem(
            currency_id=UUID("4442ca9a-172c-4e0e-ae9a-db38a1126f2d"),
            buy_calculation_type=CalculationType.ADDITION,
            buy_value=0.4,
            sell_calculation_type=CalculationType.SUBTRACTION,
            sell_value=0.3
        )
    )
    await handling_fee_provider.create_handling_fee_config_item(
        config_id=UUID("87e3e18b-2dd2-45e6-9c15-4d6b493abae6"),
        item=HandlingFeeConfigItem(
            currency_id=UUID("e002e9ef-037f-4ba5-bd8d-1d282ceacbd1"),
            buy_calculation_type=CalculationType.ADDITION,
            buy_value=0.55,
            sell_calculation_type=CalculationType.SUBTRACTION,
            sell_value=0.45
        )
    )
