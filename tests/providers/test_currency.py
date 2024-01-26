"""
Test currency provider
"""
import pytest

from app.providers import CurrencyProvider
from app.serializers.v1.currency import Currency, Currencies, PaymentMethod


@pytest.mark.asyncio
async def test_get_currencies(currency_provider: CurrencyProvider):
    """
    Test get currencies
    :param currency_provider:
    :return:
    """
    currencies = await currency_provider.get_currencies()
    assert Currencies(**currencies)


@pytest.mark.asyncio
async def test_update_currencies(currency_provider: CurrencyProvider):
    """
    Test update currencies

    :param currency_provider:
    :return:
    """
    payment_methods = [
        PaymentMethod(name="GCASH", description="GCash", sequence=1),
        PaymentMethod(name="PAYMAYA", description="PayMaya", sequence=2),
        PaymentMethod(name="BANK", description="Bank", sequence=3),
        PaymentMethod(name="PESO", description="Peso", sequence=4),
    ]
    currencies = Currencies(
        currencies=[
            Currency(name="PHP", description="Philippine Peso", sequence=1, payment_methods=payment_methods),
            Currency(name="JPY", description="Japanese Yen", sequence=2),
            Currency(name="INR", description="Indian Rupee", sequence=3),
            Currency(name="KRW", description="Korean Won", sequence=4),
            Currency(name="THB", description="Thai Baht", sequence=5),
            Currency(name="MYR", description="Malaysian Ringgit", sequence=6),
            Currency(name="USD", description="US Dollar", sequence=7),
            Currency(name="CAD", description="Canadian Dollar", sequence=8),
            Currency(name="HKD", description="Hong Kong Dollar", sequence=9),
            Currency(name="SGD", description="Singapore Dollar", sequence=10),
            Currency(name="VND", description="Vietnamese Dong", sequence=11),
            Currency(name="AUD", description="Australian Dollar", sequence=12),
            Currency(name="AED", description="United Arab Emirates Dirham", sequence=13),
            Currency(name="MMK", description="Myanmar Kyat", sequence=14),
            Currency(name="BDT", description="Bangladeshi Taka", sequence=15),
            Currency(name="BRL", description="Brazilian Real", sequence=16),
        ]
    )
    data = currencies.model_dump()
    await currency_provider.update_currencies(data=data)
