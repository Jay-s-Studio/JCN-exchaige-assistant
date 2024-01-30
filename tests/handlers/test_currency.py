"""
Test currency provider
"""
import pytest

from app.handlers import CurrencyHandler


@pytest.mark.asyncio
async def test_get_currency_tree(currency_handler: CurrencyHandler):
    """
    Test get currencies
    :param currency_handler:
    :return:
    """
    currencies = await currency_handler.get_currency_tree()
    assert currencies is not None
    assert currencies.nodes is not None
