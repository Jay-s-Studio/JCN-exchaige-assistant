"""
Test exchange rate provider
"""
import pytest

from app.providers import ExchangeRateProvider


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
