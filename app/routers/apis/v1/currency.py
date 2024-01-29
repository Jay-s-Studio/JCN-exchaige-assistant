"""
Currency API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.containers import Container
from app.handlers.currency import CurrencyHandler
from app.libs.depends import check_all_authenticators, DEFAULT_RATE_LIMITERS
from app.route_classes import LogRoute
from app.serializers.v1.currency import CurrencyInfo

router = APIRouter(
    dependencies=DEFAULT_RATE_LIMITERS,
    route_class=LogRoute
)


@router.post(
    path="/",
    dependencies=[Depends(check_all_authenticators)]
)
@inject
async def create_currency(
    currency_info: CurrencyInfo,
    currency_handler: CurrencyHandler = Depends(Provide[Container.currency_handler])
):
    """
    Update currency
    :return:
    """
    await currency_handler.create_currency(currency_info=currency_info)


@router.get(
    path="/all",
    # response_model=Currencies
)
@inject
async def all_currency(
    currency_handler: CurrencyHandler = Depends(Provide[Container.currency_handler])
):
    """
    Get all currency
    :return:
    """
    return await currency_handler.get_all_currency()
