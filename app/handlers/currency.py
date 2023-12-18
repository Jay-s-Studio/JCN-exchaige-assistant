"""
CurrencyHandler
"""
from app.providers import CurrencyProvider
from app.serializers.v1.currency import Currencies


class CurrencyHandler:
    """CurrencyHandler"""

    def __init__(self, currency_provider: CurrencyProvider):
        self.currency_provider = currency_provider

    async def get_all_currency(self):
        """
        Get all currency
        :return:
        """
        return await self.currency_provider.get_currencies()

    async def update_currencies(self, currency_list: Currencies):
        """
        Update currencies
        :return:
        """
        data = currency_list.model_dump()
        return await self.currency_provider.update_currencies(data)
