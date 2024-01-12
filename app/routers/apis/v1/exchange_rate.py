"""
ExchangeRate API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers.exchange_rate import ExchangeRateHandler
from app.libs.depends import check_all_authenticators, DEFAULT_RATE_LIMITERS
from app.route_classes import LogRoute
from app.serializers.v1.exchange_rate import UpdateExchangeRate, GroupExchangeRate

router = APIRouter(
    dependencies=DEFAULT_RATE_LIMITERS,
    route_class=LogRoute
)


@router.get(
    path="/{group_id}",
    response_model=GroupExchangeRate,
    dependencies=[Depends(check_all_authenticators)],
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
