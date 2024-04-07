"""
Test message controller.
"""
from decimal import Decimal

import pytest

from app.controllers import MessagesController
from app.libs.consts.enums import OperationType


@pytest.mark.asyncio
async def test__get_price(messages_controller: MessagesController):
    """
    Test _get_price
    :param messages_controller:
    :return:
    """
    operation_type = OperationType.BUY
    exchange_rate, handling_fee = await messages_controller._get_rate_and_fee(
        group_id=-1002050270240,
        currency="GCASH",
        operation_type=operation_type
    )
    price = await messages_controller._get_price(
        exchange_rate=exchange_rate,
        handling_fee=handling_fee,
        operation_type=operation_type
    )
    print(price)


@pytest.mark.asyncio
def test__round_to_nearest(messages_controller: MessagesController):
    """
    Test _get_rate_and_fee
    :param messages_controller:
    :return:
    """
    price = Decimal("56.17")
    result = messages_controller._round_to_nearest(price)
    print(result)
