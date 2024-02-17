"""
Currency API Router
"""
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers.currency import CurrencyHandler
from app.libs.depends import (
    check_all_authenticators,
    check_access_token,
    DEFAULT_RATE_LIMITERS,
)
from app.route_classes import LogRoute
from app.serializers.v1.currency import CurrencyInfo, CurrencyTree, Currencies, ChangeSequence

router = APIRouter(
    dependencies=DEFAULT_RATE_LIMITERS,
    route_class=LogRoute
)


@router.get(
    path="/tree",
    response_model=CurrencyTree,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_access_token)]
)
@inject
async def get_currency_tree(
    currency_handler: CurrencyHandler = Depends(Provide[Container.currency_handler])
):
    """
    Get currency tree
    :return:
    """
    return await currency_handler.get_currency_tree()


@router.get(
    path="/all",
    response_model=Currencies,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_all_authenticators)]
)
@inject
async def get_currencies(
    currency_handler: CurrencyHandler = Depends(Provide[Container.currency_handler])
):
    """
    Get currencies
    :return:
    """
    return await currency_handler.get_currencies()


@router.post(
    path="/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_access_token)]
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


@router.put(
    path="/update/{currency_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_access_token)]
)
@inject
async def update_currency(
    currency_id: UUID,
    currency_info: CurrencyInfo,
    currency_handler: CurrencyHandler = Depends(Provide[Container.currency_handler])
):
    """
    Update currency
    :return:
    """
    await currency_handler.update_currency(currency_id=currency_id, currency_info=currency_info)


@router.put(
    path="/change_sequence",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_access_token)]
)
@inject
async def change_sequence(
    model: ChangeSequence,
    currency_handler: CurrencyHandler = Depends(Provide[Container.currency_handler])
):
    """
    Change sequence
    :return:
    """
    await currency_handler.change_sequence(model=model)
