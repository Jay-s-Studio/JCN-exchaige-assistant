"""
ExchangeRateHandler
"""
from app.providers import ExchangeRateProvider
from app.serializers.v1.exchange_rate import UpdateExchangeRate


class ExchangeRateHandler:
    """ExchangeRateHandler"""

    def __init__(self, exchange_rate_provider: ExchangeRateProvider):
        self.exchange_rate_provider = exchange_rate_provider

    async def get_exchange_rate(self, group_id: str):
        """
        Get exchange rate
        :return:
        """
        result = await self.exchange_rate_provider.get_exchange_rate(group_id=group_id)
        return result

    async def update_exchange_rate(self, model: UpdateExchangeRate):
        """
        Update exchange rate
        :return:
        """
        return await self.exchange_rate_provider.update_exchange_rate(
            group_id=model.group_id,
            currency_rates={"currency_rates": [currency_rate.model_dump() for currency_rate in model.currency_rates]}
        )
