"""
Test handling fee provider
"""
from uuid import UUID

import pytest

from app.libs.consts.enums import CalculationType, OperationType
from app.providers import HandingFeeProvider
from app.serializers.v1.handing_fee import HandingFeeConfig, HandingFeeConfigItem


@pytest.mark.asyncio
async def test_get_handing_fee_config_page(
    handing_fee_provider: HandingFeeProvider
):
    """
    Test get handing fee config page
    """
    config, total = await handing_fee_provider.get_handing_fee_config_page(0, 10)
    assert config, total


@pytest.mark.asyncio
async def test_get_handing_fee_config(
    handing_fee_provider: HandingFeeProvider
):
    """
    Test get handing fee config
    """
    config = await handing_fee_provider.get_handing_fee_config(UUID("87e3e18b-2dd2-45e6-9c15-4d6b493abae6"))
    assert config


@pytest.mark.asyncio
async def test_get_global_handing_fee_config(
    handing_fee_provider: HandingFeeProvider
):
    """
    Test get global handing fee config
    """
    config = await handing_fee_provider.get_global_handing_fee_config()
    assert config <= 1


@pytest.mark.asyncio
async def test_create_handing_fee_config(
    handing_fee_provider: HandingFeeProvider
):
    """
    Test create handing fee config
    """
    config = HandingFeeConfig(
        id=UUID("87e3e18b-2dd2-45e6-9c15-4d6b493abae6"),
        name="Test",
        items=[]
    )
    await handing_fee_provider.create_handing_fee_config(config)


@pytest.mark.asyncio
async def test_create_handing_fee_config_item(
    handing_fee_provider: HandingFeeProvider
):
    """
    Test create handing fee config item
    """
    await handing_fee_provider.create_handing_fee_config_item(
        config_id=UUID("87e3e18b-2dd2-45e6-9c15-4d6b493abae6"),
        item=HandingFeeConfigItem(
            currency_id=UUID("4442ca9a-172c-4e0e-ae9a-db38a1126f2d"),
            buy_calculation_type=CalculationType.ADDITION,
            buy_value=0.4,
            sell_calculation_type=CalculationType.SUBTRACTION,
            sell_value=0.3
        )
    )
    await handing_fee_provider.create_handing_fee_config_item(
        config_id=UUID("87e3e18b-2dd2-45e6-9c15-4d6b493abae6"),
        item=HandingFeeConfigItem(
            currency_id=UUID("e002e9ef-037f-4ba5-bd8d-1d282ceacbd1"),
            buy_calculation_type=CalculationType.ADDITION,
            buy_value=0.55,
            sell_calculation_type=CalculationType.SUBTRACTION,
            sell_value=0.45
        )
    )
