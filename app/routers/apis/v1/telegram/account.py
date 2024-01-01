"""
Telegram Account API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query

from app.containers import Container
from app.handlers.telegram import TelegramAccountHandler
from app.libs.auth import check_all_authenticators
from app.routing import LogRouting

router = APIRouter(
    dependencies=[Depends(check_all_authenticators)],
    route_class=LogRouting
)


@router.get(
    path="/groups"
)
@inject
async def get_accounts(
    page_size: int = Query(default=20, description="Page Size", lt=100, gt=0),
    page_index: int = Query(default=0, description="Page Index", ge=0),
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param page_size:
    :param page_index:
    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.get_groups(
        page_size=page_size,
        page_index=page_index
    )


@router.get(
    path="/vendors"
)
@inject
async def get_vendors(
    page_size: int = Query(default=20, description="Page Size", lt=100, gt=0),
    page_index: int = Query(default=0, description="Page Index", ge=0),
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param page_size:
    :param page_index:
    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.get_vendors(
        page_size=page_size,
        page_index=page_index
    )


@router.get(
    path="/customers"
)
@inject
async def get_customers(
    page_size: int = Query(default=20, description="Page Size", lt=100, gt=0),
    page_index: int = Query(default=0, description="Page Index", ge=0),
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param page_size:
    :param page_index:
    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.get_customers(
        page_size=page_size,
        page_index=page_index
    )
