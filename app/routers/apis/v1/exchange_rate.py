"""
ExchangeRate API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers.exchange_rate import ExchangeRateHandler
from app.libs.depends import (
    check_api_key_authenticator,
    check_access_token,
    DEFAULT_RATE_LIMITERS,
)
from app.route_classes import LogRoute
from app.serializers.v1.exchange_rate import UpdateExchangeRate, ExchangeRateResponse

router = APIRouter(
    dependencies=DEFAULT_RATE_LIMITERS,
    route_class=LogRoute
)


@router.get(
    path="/{group_id}",
    response_model=ExchangeRateResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_access_token)]
)
@inject
async def get_exchange_rate(
    group_id: int,
    exchange_rate_handler: ExchangeRateHandler = Depends(Provide[Container.exchange_rate_handler])
):
    """
    Get currency rate
    :return:
    """
    return await exchange_rate_handler.get_exchange_rate(group_id=group_id)


@router.post(
    path="/currency_rate",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_api_key_authenticator)]
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
