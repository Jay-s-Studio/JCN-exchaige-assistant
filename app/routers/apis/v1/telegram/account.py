"""
Telegram Account API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query
from starlette import status

from app.containers import Container
from app.handlers.telegram import TelegramAccountHandler
from app.libs.depends import check_all_authenticators, DEFAULT_RATE_LIMITERS
from app.route_classes import LogRoute
from app.serializers.v1.telegram import (
    GroupsResponse,
    GroupMembersResponse,
    CustomerResponse,
    VendorResponse,
    TelegramGroup,
    UpdateTelegramGroup,
)

router = APIRouter(
    dependencies=[
        Depends(check_all_authenticators),
        *DEFAULT_RATE_LIMITERS
    ],
    route_class=LogRoute
)


@router.get(
    path="/groups",
    response_model=GroupsResponse,
    status_code=status.HTTP_200_OK
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
    path="/vendors",
    response_model=VendorResponse,
    status_code=status.HTTP_200_OK
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
    path="/customers",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK
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


@router.get(
    path="/group/{group_id}",
    response_model=TelegramGroup,
    status_code=status.HTTP_200_OK
)
@inject
async def get_group(
    group_id: str,
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param group_id:
    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.get_group(
        group_id=group_id
    )


@router.put(
    path="/group/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def update_group(
    group_id: str,
    model: UpdateTelegramGroup,
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param group_id:
    :param model:
    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.update_group(
        group_id=group_id,
        model=model
    )


@router.get(
    path="/group/{group_id}/members",
    response_model=GroupMembersResponse,
    status_code=status.HTTP_200_OK
)
@inject
async def get_group_members(
    group_id: int,
    page_size: int = Query(default=20, description="Page Size", lt=100, gt=0),
    page_index: int = Query(default=0, description="Page Index", ge=0),
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param group_id:
    :param page_size:
    :param page_index:
    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.get_group_members(
        group_id=group_id,
        page_size=page_size,
        page_index=page_index
    )
