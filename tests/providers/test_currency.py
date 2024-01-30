"""
Test currency provider
"""
from uuid import UUID

import pytest

from app.libs.consts.enums import CurrencyType
from app.providers import CurrencyProvider
from app.schemas.currency import Currency

PHP = Currency(
    id=UUID("5589c1fe-353b-4684-8b46-7580c9046c55"),
    symbol="PHP",
    path="5589c1fe-353b-4684-8b46-7580c9046c55",
    description="Philippine Peso"
)
GCASH = Currency(
    id=UUID("4442ca9a-172c-4e0e-ae9a-db38a1126f2d"),
    type=CurrencyType.PAYMENT,
    symbol="GCASH",
    path=f"{PHP.id}/4442ca9a-172c-4e0e-ae9a-db38a1126f2d",
    description="GCash",
    parent_id=PHP.id
)
PAYMAYA = Currency(
    id=UUID("7a6b2811-3c3b-4e45-9b43-5b25b24a8921"),
    type=CurrencyType.PAYMENT,
    symbol="PAYMAYA",
    path=f"{PHP.id}/7a6b2811-3c3b-4e45-9b43-5b25b24a8921",
    description="PayMaya",
    parent_id=PHP.id
)
BANK = Currency(
    id=UUID("e8c74abf-8e93-46e1-b266-8e30ce98cf58"),
    type=CurrencyType.PAYMENT,
    symbol="BANK",
    path=f"{PHP.id}/e8c74abf-8e93-46e1-b266-8e30ce98cf58",
    description="Bank",
    parent_id=PHP.id
)
PESO = Currency(
    id=UUID("e002e9ef-037f-4ba5-bd8d-1d282ceacbd1"),
    type=CurrencyType.PAYMENT,
    symbol="PESO",
    path=f"{PHP.id}/e002e9ef-037f-4ba5-bd8d-1d282ceacbd1",
    description="Peso",
    parent_id=PHP.id
)
JPY = Currency(
    id=UUID("8086f3da-436b-4535-8f0c-d8859f68f626"),
    symbol="JPY",
    path="8086f3da-436b-4535-8f0c-d8859f68f626",
    description="Japanese Yen"
)
INR = Currency(
    id=UUID("b6d698a1-10d0-407c-829c-4bf1f6550010"),
    symbol="INR",
    path="b6d698a1-10d0-407c-829c-4bf1f6550010",
    description="Indian Rupee"
)
KRW = Currency(
    id=UUID("6e6d3734-5d2a-4275-bfa4-b1245b577b89"),
    symbol="KRW",
    path="6e6d3734-5d2a-4275-bfa4-b1245b577b89",
    description="Korean Won"
)
THB = Currency(
    id=UUID("063f36cc-1fdc-4cd3-8671-be66c4b5a0ef"),
    symbol="THB",
    path="063f36cc-1fdc-4cd3-8671-be66c4b5a0ef",
    description="Thai Baht"
)
MYR = Currency(
    id=UUID("cb078df3-89e1-428a-81d0-23dc81aa56ad"),
    symbol="MYR",
    path="cb078df3-89e1-428a-81d0-23dc81aa56ad",
    description="Malaysian Ringgit"
)
USD = Currency(
    id=UUID("8d5fb194-2146-4627-a2d7-0561c73ce257"),
    symbol="USD",
    path="8d5fb194-2146-4627-a2d7-0561c73ce257",
    description="US Dollar"
)
CAD = Currency(
    id=UUID("d136040c-b750-4567-8100-0676ef6e974b"),
    symbol="CAD",
    path="d136040c-b750-4567-8100-0676ef6e974b",
    description="Canadian Dollar"
)
HKD = Currency(
    id=UUID("2c026900-3071-4174-874f-bb09f409a42d"),
    symbol="HKD",
    path="2c026900-3071-4174-874f-bb09f409a42d",
    description="Hong Kong Dollar"
)
SGD = Currency(
    id=UUID("4a17441c-fe66-4e89-b7cd-1097042c9160"),
    symbol="SGD",
    path="4a17441c-fe66-4e89-b7cd-1097042c9160",
    description="Singapore Dollar"
)
VND = Currency(
    id=UUID("a61d81de-393b-4b35-b349-032a0c06f424"),
    symbol="VND",
    path="a61d81de-393b-4b35-b349-032a0c06f424",
    description="Vietnamese Dong"
)
AUD = Currency(
    id=UUID("b0bbe334-7e92-4670-b110-135b5dd8095e"),
    symbol="AUD",
    path="b0bbe334-7e92-4670-b110-135b5dd8095e",
    description="Australian Dollar"
)
AED = Currency(
    id=UUID("14286957-4aa8-4957-954b-5dae9f73a244"),
    symbol="AED",
    path="14286957-4aa8-4957-954b-5dae9f73a244",
    description="United Arab Emirates Dirham"
)
MMK = Currency(
    id=UUID("5b634b1c-e1ac-40d3-b418-03a2f8098806"),
    symbol="MMK",
    path="5b634b1c-e1ac-40d3-b418-03a2f8098806",
    description="Myanmar Kyat"
)
BDT = Currency(
    id=UUID("1edaaa1a-2c00-4727-a25d-a23328687d62"),
    symbol="BDT",
    path="1edaaa1a-2c00-4727-a25d-a23328687d62",
    description="Bangladeshi Taka"
)
BRL = Currency(
    id=UUID("19edc056-9344-4194-936d-144e3f982534"),
    symbol="BRL",
    path="19edc056-9344-4194-936d-144e3f982534",
    description="Brazilian Real"
)


@pytest.mark.asyncio
async def test_create_currency(currency_provider: CurrencyProvider):
    """
    Test create currency
    :param currency_provider:
    :return:
    """
    currency = PHP
    await currency_provider.create_currency(currency=currency)


@pytest.mark.asyncio
async def test_create_currencies(currency_provider: CurrencyProvider):
    """
    Test create currencies
    :param currency_provider:
    :return:
    """
    currencies = [
        PHP, GCASH, PAYMAYA, BANK, PESO,
        JPY, INR, KRW, THB, MYR, USD, CAD, HKD, SGD, VND, AUD, AED, MMK, BDT, BRL
    ]
    for currency in currencies:
        await currency_provider.create_currency(currency=currency)


@pytest.mark.asyncio
async def test_update_currency(currency_provider: CurrencyProvider):
    """
    Test update currency

    :param currency_provider:
    :return:
    """
    currency = PHP
    currency.description = "Philippine Peso 123"
    await currency_provider.update_currency(currency=currency)


@pytest.mark.asyncio
async def test_get_currencies(currency_provider: CurrencyProvider):
    """
    Test get currencies
    :param currency_provider:
    :return:
    """
    currencies = await currency_provider.get_currency_tree_data()
    assert isinstance(currencies, list)
