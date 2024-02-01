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
    TelegramAccount,
    TelegramChatGroup,
    VendorResponse,
    GroupMemberBase,
    InitGroupMember, GroupList,
)

router = APIRouter(
    dependencies=[
        Depends(check_all_authenticators),
        *DEFAULT_RATE_LIMITERS
    ],
    route_class=LogRoute
)


@router.post(
    path="/raw/account",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Vendors Bot API"]
)
@inject
async def set_account(
    telegram_account: TelegramAccount,
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param telegram_account:
    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.set_account(telegram_account=telegram_account)


@router.post(
    path="/raw/group",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Vendors Bot API"]
)
@inject
async def set_group(
    telegram_group: TelegramChatGroup,
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param telegram_group:
    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.set_group(telegram_group=telegram_group)


@router.post(
    path="/init_chat_group_member",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Vendors Bot API"]
)
@inject
async def init_chat_group_member(
    model: InitGroupMember,
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param model:
    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.init_chat_group_member(model=model)


@router.delete(
    path="/delete_chat_group_member",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Vendors Bot API"]
)
@inject
async def delete_chat_group_member(
    model: GroupMemberBase,
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param model:
    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.delete_chat_group_member(
        account_id=model.account_id,
        group_id=model.group_id
    )


@router.get(
    path="/vendors",
    response_model=VendorResponse,
    status_code=status.HTTP_200_OK,
    tags=["Vendors Bot API"]
)
@inject
async def get_vendors(
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.get_vendors()


@router.get(
    path="/groups",
    response_model=GroupList,
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
    return await telegram_account_handler.get_chat_groups(
        page_size=page_size,
        page_index=page_index
    )


@router.get(
    path="/group/{group_id}",
    status_code=status.HTTP_200_OK
)
@inject
async def get_group(
    group_id: int,
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param group_id:
    :param telegram_account_handler:
    :return:
    """


@router.put(
    path="/group/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def update_group(
    group_id: int,
    # model: UpdateTelegramGroup,
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param group_id:
    :param model:
    :param telegram_account_handler:
    :return:
    """


@router.get(
    path="/group/{group_id}/members",
    status_code=status.HTTP_200_OK
)
@inject
async def get_all_chat_group_members(
    group_id: int,
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param group_id:
    :param telegram_account_handler:
    :return:
    """
