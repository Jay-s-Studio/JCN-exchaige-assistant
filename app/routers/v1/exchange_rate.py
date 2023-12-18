"""ExchangeRate Router"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers.exchange_rate import ExchangeRateHandler
from app.serializers.v1.exchange_rate import UpdateExchangeRate

router = APIRouter()


@router.post(
    path="/currency_rate",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def update_currency_rate(
    model: UpdateExchangeRate,
    exchange_rate_handler: ExchangeRateHandler = Depends(Provide[Container.exchange_rate_handler])
):
    """
    Update currency rate
    :return:
    """
    await exchange_rate_handler.update_exchange_rate(model=model)
