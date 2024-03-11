"""
Test order provider
"""
from datetime import datetime, timedelta
from uuid import UUID

import pytest
import pytz

from app.libs.consts.enums import Language, OrderStatus
from app.providers import OrderProvider
from app.schemas.order import Cart, Order


@pytest.mark.asyncio
async def test_get_order_page(order_provider: OrderProvider):
    """
    get order page
    :param order_provider:
    :return:
    """
    result, count = await order_provider.get_order_page()
    assert result
    assert len(result) == count
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_create_cart(order_provider: OrderProvider):
    """
    create cart
    :param order_provider:
    :return:
    """
    cart = Cart(
        id=UUID("c3ef8919-dc0b-4166-a4a5-907cfc266978"),
        message_id=1,
        group_name="Customers - DEV",
        group_id=-1002050270240,
        vendor_name="Vendors - DEV",
        vendor_id=-1002003483337,
        account_name="jayhsia",
        account_id=1259597115,
        payment_currency="GCASH",
        payment_amount=100000,
        exchange_currency="USDT",
        original_exchange_rate=56.7,
        with_fee_exchange_rate=57.3
    )
    cart_id = await order_provider.create_cart(cart=cart)
    print(cart_id)
    assert cart_id
    assert cart_id == cart.id


@pytest.mark.asyncio
async def test_generate_order_no(order_provider: OrderProvider):
    """
    generate order no
    :param order_provider:
    :return:
    """
    order_no = await order_provider.generate_order_no()
    assert order_no
    assert isinstance(order_no, str)
    assert len(order_no) == 16


@pytest.mark.asyncio
async def test_create_order(order_provider: OrderProvider):
    """
    create order
    :param order_provider:
    :return:
    """
    now = datetime.now(tz=pytz.UTC)
    order = Order(
        cart_id=UUID("c3ef8919-dc0b-4166-a4a5-907cfc266978"),
        expiration_of_pay=now + timedelta(hours=1),
    )
    order_no = await order_provider.create_order(order=order)
    assert order_no[1:9] == now.strftime('%Y%m%d')


@pytest.mark.asyncio
async def test_update_order_description(order_provider: OrderProvider):
    """
    update order description
    :param order_provider:
    :return:
    """
    order_no = "O202403110000001"
    description = "test"
    await order_provider.update_order_description(order_no=order_no, description=description)
