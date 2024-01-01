"""
Test handling fee provider
"""
import pytest

from app.providers import HandingFeeProvider


@pytest.mark.asyncio
async def test_set_global_handing_fee(handing_fee_provider: HandingFeeProvider):
    """
    test set global handing fee
    :param handing_fee_provider:
    :return:
    """
    await handing_fee_provider.set_global_handing_fee(
        data={
            "buying_fee": 0.05,
            "selling_fee": 0.04
        }
    )


@pytest.mark.asyncio
async def test_get_global_handing_fee(handing_fee_provider: HandingFeeProvider):
    """
    test get global handing fee
    :param handing_fee_provider:
    :return:
    """
    handing_fee = await handing_fee_provider.get_global_handing_fee()
    assert handing_fee is not None


@pytest.mark.asyncio
async def test_set_handing_fee(handing_fee_provider: HandingFeeProvider):
    """
    test set handing fee
    :param handing_fee_provider:
    :return:
    """
    handing_fee = await handing_fee_provider.update_handing_fee(
        group_id="-1002050270240",
        data={
            "buying_fee": 0.05,
            "selling_fee": 0.04
        }
    )
    assert handing_fee is None


@pytest.mark.asyncio
async def test_get_handing_fee(handing_fee_provider: HandingFeeProvider):
    """
    test get handing fee
    :param handing_fee_provider:
    :return:
    """
    handing_fee = await handing_fee_provider.get_handing_fee(group_id="-1002050270240")
    assert handing_fee is not None

