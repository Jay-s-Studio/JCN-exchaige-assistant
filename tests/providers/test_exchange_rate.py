"""
Test exchange rate provider
"""
import pytest

from app.libs.consts.enums import OperationType
from app.providers import ExchangeRateProvider


@pytest.mark.asyncio
async def test_get_all_exchange_rate(exchange_rate_provider: ExchangeRateProvider):
    """
    Test get_all_exchange_rate
    :param exchange_rate_provider:
    :return:
    """
    result = await exchange_rate_provider.get_all_exchange_rate()
    assert result is not None


@pytest.mark.asyncio
async def test_get_exchange_rate(exchange_rate_provider: ExchangeRateProvider):
    """
    Test get_exchange_rate
    :param exchange_rate_provider:
    :return:
    """
    group_id = -1002003483337
    result = await exchange_rate_provider.get_exchange_rate(group_id=group_id)
    assert result is not None


@pytest.mark.asyncio
async def test_get_lowest_buying_exchange_rate(exchange_rate_provider: ExchangeRateProvider):
    """
    Test get_lowest_buying_exchange_rate
    :param exchange_rate_provider:
    :return:
    """
    currency = "GCASH"
    operation_type = OperationType.BUY
    result = await exchange_rate_provider.get_optimal_exchange_rate(
        currency=currency,
        operation_type=operation_type
    )
    assert result is not None
