"""
Test price provider.
"""
import pytest

from app.libs.consts.enums import OperationType
from app.providers import PriceProvider


@pytest.mark.asyncio
async def test_get_price_info(price_provider: PriceProvider):
    """
    Test get_price_info
    :param price_provider:
    :return:
    """
    group_id = -1002050270240
    currency = "GCASH"
    operation_type = OperationType.BUY
    price_info = await price_provider.get_price_info(
        group_id=group_id,
        currency=currency,
        operation_type=operation_type
    )
    print(price_info)
