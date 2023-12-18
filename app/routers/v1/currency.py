"""
Currency Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.containers import Container
from app.handlers.currency import CurrencyHandler
from app.serializers.v1.currency import Currencies

router = APIRouter()


@router.get(
    path="/all",
    response_model=Currencies,
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


@router.post(path="/update")
@inject
async def update_currencies(
    currency_list: Currencies,
    currency_handler: CurrencyHandler = Depends(Provide[Container.currency_handler])
):
    """
    Update currencies
    :return:
    """
    await currency_handler.update_currencies(currency_list=currency_list)
