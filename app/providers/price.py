"""
PriceProvider
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional
from uuid import UUID

from app.libs.consts.enums import CalculationType, OperationType
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.utils.calculator import Calculator
from app.providers import ExchangeRateProvider, HandlingFeeProvider
from app.schemas.exchange_rate import OptimalExchangeRate
from app.schemas.price import PriceInfo
from app.serializers.v1.handling_fee import HandlingFeeConfigItem


class PriceProvider:
    """PriceProvider"""

    def __init__(
        self,
        exchange_rate_provider: ExchangeRateProvider,
        handling_fee_provider: HandlingFeeProvider
    ):
        self._exchange_rate_provider = exchange_rate_provider
        self._handling_fee_provider = handling_fee_provider

    @distributed_trace()
    async def get_price_info(
        self,
        group_id: int,
        currency: str,
        operation_type: OperationType
    ) -> Optional[PriceInfo]:
        """
        get price info
        :param group_id:
        :param currency:
        :param operation_type:
        :return:
        """
        exchange_rate = await self.get_exchange_rate(
            currency=currency,
            operation_type=operation_type
        )
        if not exchange_rate:
            return None
        handling_fee = await self.get_handling_fee_config(
            group_id=group_id,
            currency_id=exchange_rate.currency_id
        )

        calculation_type = handling_fee.buy_calculation_type if operation_type == OperationType.BUY else handling_fee.sell_calculation_type
        rate = exchange_rate.buy_rate if operation_type == OperationType.BUY else exchange_rate.sell_rate
        price = self.calculate_fee(
            calculation_type=calculation_type,
            rate=rate,
            fee=handling_fee.buy_value if operation_type == OperationType.BUY else handling_fee.sell_value
        )
        return PriceInfo(
            vendor_name=exchange_rate.group_name,
            vendor_id=exchange_rate.group_id,
            original_rate=rate,
            price=price,
        )

    @distributed_trace()
    async def get_exchange_rate(
        self,
        currency: str,
        operation_type: OperationType
    ) -> Optional[OptimalExchangeRate]:
        """

        :param currency:
        :param operation_type:
        :return:
        """
        exchange_rate = await self._exchange_rate_provider.get_optimal_exchange_rate(
            currency=currency,
            operation_type=operation_type
        )
        if not exchange_rate:
            return None
        return exchange_rate

    @distributed_trace()
    async def get_handling_fee_config(
        self,
        group_id: int,
        currency_id: UUID
    ) -> HandlingFeeConfigItem:
        """

        :param group_id:
        :param currency_id:
        :return:
        """
        handling_fee = await self._handling_fee_provider.get_handling_fee_item_by_group_and_currency(
            group_id=group_id,
            currency_id=currency_id
        )
        if not handling_fee:
            handling_fee = await self._handling_fee_provider.get_handing_fee_global_item_by_currency(
                currency_id=currency_id
            )
        return handling_fee

    @staticmethod
    def calculate_fee(
        calculation_type: CalculationType,
        rate: float,
        fee: float
    ) -> float:
        """
        calculate fee
        :param calculation_type:
        :param rate:
        :param fee:
        :return:
        """
        d_rate, d_fee = Decimal(str(rate)), Decimal(str(fee))
        base = Decimal('0.05')
        match calculation_type:
            case CalculationType.ADDITION:
                result = d_rate + d_fee
            case CalculationType.SUBTRACTION:
                result = d_rate - d_fee
            case CalculationType.MULTIPLICATION:
                result = d_rate * d_fee
            case CalculationType.DIVISION:
                result = d_rate / d_fee
            case _:
                result = d_rate

        round_result = Calculator.round_to_nearest(price=result, base=base)
        return float(round_result)

