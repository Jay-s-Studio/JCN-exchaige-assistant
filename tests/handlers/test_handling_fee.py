"""
Test handling fee handler
"""
from uuid import UUID

import pytest

from app.handlers.handling_fee import HandlingFeeHandler
from app.libs.consts.enums import CalculationType
from app.serializers.v1.handling_fee import HandlingFeeConfig, HandlingFeeConfigItem


@pytest.mark.asyncio
async def test_get_handling_fee_config_page(
    handling_fee_handler: HandlingFeeHandler
):
    """
    Test get handling fee config page
    """
    configs = await handling_fee_handler.get_handling_fee_config_page(0, 10)
    assert configs


@pytest.mark.asyncio
async def test_get_handling_fee_config(
    handling_fee_handler: HandlingFeeHandler
):
    """
    Test get handling fee config
    """
    config_id = UUID("87e3e18b-2dd2-45e6-9c15-4d6b493abae6")
    config = await handling_fee_handler.get_handling_fee_config(config_id)
    assert config


@pytest.mark.asyncio
async def test_create_handling_fee_config(
    handling_fee_handler: HandlingFeeHandler
):
    """
    Test create handling fee config
    """
    config = HandlingFeeConfig(
        id=UUID("73a80953-f74e-431e-8e93-8001e57ad947"),
        name="For PHP",
        items=[
            HandlingFeeConfigItem(
                currency_id=UUID("5589c1fe-353b-4684-8b46-7580c9046c55"),
                buy_calculation_type=CalculationType.ADDITION,
                buy_value=0.4,
                sell_calculation_type=CalculationType.SUBTRACTION,
                sell_value=0.7
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("e8c74abf-8e93-46e1-b266-8e30ce98cf58"),
                buy_calculation_type=CalculationType.ADDITION,
                buy_value=0.4,
                sell_calculation_type=CalculationType.SUBTRACTION,
                sell_value=0.7
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("e002e9ef-037f-4ba5-bd8d-1d282ceacbd1"),
                buy_calculation_type=CalculationType.ADDITION,
                buy_value=0.4,
                sell_calculation_type=CalculationType.SUBTRACTION,
                sell_value=0.7
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("8086f3da-436b-4535-8f0c-d8859f68f626"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("b6d698a1-10d0-407c-829c-4bf1f6550010"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("6e6d3734-5d2a-4275-bfa4-b1245b577b89"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("063f36cc-1fdc-4cd3-8671-be66c4b5a0ef"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("cb078df3-89e1-428a-81d0-23dc81aa56ad"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("8d5fb194-2146-4627-a2d7-0561c73ce257"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("d136040c-b750-4567-8100-0676ef6e974b"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("2c026900-3071-4174-874f-bb09f409a42d"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("4a17441c-fe66-4e89-b7cd-1097042c9160"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("a61d81de-393b-4b35-b349-032a0c06f424"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("b0bbe334-7e92-4670-b110-135b5dd8095e"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("14286957-4aa8-4957-954b-5dae9f73a244"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("5b634b1c-e1ac-40d3-b418-03a2f8098806"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("1edaaa1a-2c00-4727-a25d-a23328687d62"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("19edc056-9344-4194-936d-144e3f982534"),
                buy_calculation_type=CalculationType.MULTIPLICATION,
                buy_value=1.01,
                sell_calculation_type=CalculationType.DIVISION,
                sell_value=1.01
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("4442ca9a-172c-4e0e-ae9a-db38a1126f2d"),
                buy_calculation_type=CalculationType.ADDITION,
                buy_value=0.4,
                sell_calculation_type=CalculationType.SUBTRACTION,
                sell_value=0.7
            ),
            HandlingFeeConfigItem(
                currency_id=UUID("7a6b2811-3c3b-4e45-9b43-5b25b24a8921"),
                buy_calculation_type=CalculationType.ADDITION,
                buy_value=0.4,
                sell_calculation_type=CalculationType.SUBTRACTION,
                sell_value=0.7
            ),
        ]
    )
    await handling_fee_handler.create_handling_fee_config(config)
