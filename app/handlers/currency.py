"""
CurrencyHandler
"""
from app.libs.consts.enums import CurrencyType
from app.libs.decorators.sentry_tracer import distributed_trace
from app.providers import CurrencyProvider
from app.schemas.currency import Currency
from app.serializers.v1.currency import CurrencyInfo


class CurrencyHandler:
    """CurrencyHandler"""

    def __init__(self, currency_provider: CurrencyProvider):
        self.currency_provider = currency_provider

    @distributed_trace()
    async def create_currency(self, currency_info: CurrencyInfo):
        """
        Update currency
        :return:
        """
        currency = Currency(
            **currency_info.model_dump(),
            type=CurrencyType.PAYMENT if currency_info.parent_id else CurrencyType.GENERAL,
            path=f"{currency_info.parent_id}/{currency_info.id}" if currency_info.parent_id else currency_info.id
        )
        return await self.currency_provider.create_currency(currency=currency)

    @distributed_trace()
    async def get_all_currency(self):
        """
        Get all currency
        :return:
        """
        return await self.currency_provider.get_currencies()
