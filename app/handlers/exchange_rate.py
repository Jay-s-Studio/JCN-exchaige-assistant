"""
ExchangeRateHandler
"""
from starlette import status

from app.exceptions.api_base import APIException
from app.providers import ExchangeRateProvider
from app.serializers.v1.exchange_rate import UpdateExchangeRate, GroupExchangeRate


class ExchangeRateHandler:
    """ExchangeRateHandler"""

    def __init__(self, exchange_rate_provider: ExchangeRateProvider):
        self.exchange_rate_provider = exchange_rate_provider

    async def get_exchange_rate(self, group_id: str) -> GroupExchangeRate:
        """
        Get exchange rate
        :return:
        """
        result = await self.exchange_rate_provider.get_exchange_rate(group_id=group_id)
        if result is None:
            raise APIException(status_code=status.HTTP_404_NOT_FOUND, message="Group not found")
        return GroupExchangeRate(
            **result,
            group_id=group_id
        )

    async def update_exchange_rate(self, model: UpdateExchangeRate):
        """
        Update exchange rate
        :return:
        """
        return await self.exchange_rate_provider.update_exchange_rate(
            group_id=model.group_id,
            exchange_rates={"exchange_rates": [currency_rate.model_dump() for currency_rate in model.currency_rates]}
        )
