"""ExchangeRate Router"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers.exchange_rate import ExchangeRateHandler
from app.libs.auth.bearer_jwt import BearerJWTAuth
from app.routing import LogRouting
from app.serializers.v1.exchange_rate import UpdateExchangeRate, GetExchangeRate

router = APIRouter(route_class=LogRouting)


@router.get(
    path="/{group_id}",
    response_model=GetExchangeRate,
    dependencies=[Depends(BearerJWTAuth())],
)
@inject
async def get_exchange_rate(
    group_id: str,
    exchange_rate_handler: ExchangeRateHandler = Depends(Provide[Container.exchange_rate_handler])
):
    """
    Get currency rate
    :return:
    """
    return await exchange_rate_handler.get_exchange_rate(group_id=group_id)


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
