"""
ExchangeRateHandler
"""
from app.libs.decorators.sentry_tracer import distributed_trace
from app.libs.logger import logger
from app.providers import ExchangeRateProvider
from app.serializers.v1.exchange_rate import UpdateExchangeRate, ExchangeRateResponse


class ExchangeRateHandler:
    """ExchangeRateHandler"""

    def __init__(self, exchange_rate_provider: ExchangeRateProvider):
        self.exchange_rate_provider = exchange_rate_provider

    @distributed_trace()
    async def get_exchange_rate(self, group_id: int) -> ExchangeRateResponse:
        """
        Get exchange rate
        :return:
        """
        result = await self.exchange_rate_provider.get_exchange_rate(group_id=group_id)
        return ExchangeRateResponse(exchange_rates=result)

    @distributed_trace()
    async def update_exchange_rate(self, model: UpdateExchangeRate):
        """
        Update exchange rate
        :return:
        """
        for exchange_rate in model.currency_rates:
            try:
                await self.exchange_rate_provider.update_exchange_rate(
                    group_id=model.group_id,
                    exchange_rate=exchange_rate.model_dump()
                )
            except Exception as e:
                logger.error(e)
                continue
