"""
Telegram Account API Router
"""
from typing import Optional
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query
from starlette import status

from app.containers import Container
from app.exceptions.api_base import ApiBaseException
from app.handlers.telegram import TelegramAccountHandler
from app.libs.consts.enums import BotType, PaymentAccountStatus
from app.libs.depends import (
    check_all_authenticators,
    check_api_key_authenticator,
    check_access_token,
    DEFAULT_RATE_LIMITERS,
)
from app.route_classes import LogRoute
from app.serializers.v1.telegram import (
    TelegramAccount,
    TelegramChatGroup,
    VendorResponse,
    GroupMemberBase,
    InitGroupMember,
    GroupInfo,
    GroupPage,
    GroupList,
    GroupMembers,
    UpdateGroupInfo,
    GroupQuery,
)

router = APIRouter(
    dependencies=DEFAULT_RATE_LIMITERS,
    route_class=LogRoute
)


def parse_uuid_list(
    group_type_ids: str = Query(default=None, description="Group Type IDs (multiple values separated by comma)")
) -> Optional[list[UUID]]:
    """

    :param group_type_ids:
    :return:
    """
    if group_type_ids is None:
        return

    try:
        return [UUID(group_type_id) for group_type_id in group_type_ids.split(",")]
    except ValueError:
        raise ApiBaseException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid format."
        )


@router.post(
    path="/raw/account",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Vendors Bot API"],
    dependencies=[Depends(check_api_key_authenticator)]
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
    tags=["Vendors Bot API"],
    dependencies=[Depends(check_api_key_authenticator)]
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
    tags=["Vendors Bot API"],
    dependencies=[Depends(check_api_key_authenticator)]
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
    tags=["Vendors Bot API"],
    dependencies=[Depends(check_api_key_authenticator)]
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
    tags=["Vendors Bot API"],
    dependencies=[Depends(check_all_authenticators)]
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
    path="/groups_by_type",
    response_model=GroupList,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_access_token)]
)
@inject
async def get_chat_groups_by_type(
    group_type: BotType,
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param group_type:
    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.get_chat_groups_by_type(group_type=group_type)


@router.get(
    path="/groups",
    response_model=GroupPage,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_access_token)]
)
@inject
async def get_chat_groups(
    page_size: int = Query(default=20, description="Page Size", lt=100, gt=0),
    page_index: int = Query(default=0, description="Page Index", ge=0),
    title: str = Query(default=None, description="Title"),
    bot_type: BotType = Query(default=None, description="Bot Type"),
    in_group: bool = Query(default=None, description="In Group"),
    payment_account_status: PaymentAccountStatus = Query(default=None, description="Payment Account Status"),
    currency_id: UUID = Query(default=None, description="Currency ID"),
    handling_fee_config_id: UUID = Query(default=None, description="Handling Fee Config ID"),
    group_type_ids: list[UUID] = Depends(parse_uuid_list),
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param page_size:
    :param page_index:
    :param title:
    :param bot_type:
    :param in_group:
    :param payment_account_status:
    :param currency_id:
    :param handling_fee_config_id:
    :param group_type_ids:
    :param telegram_account_handler:
    :return:
    """
    group_query = GroupQuery(
        page_size=page_size,
        page_index=page_index,
        title=title,
        bot_type=bot_type,
        in_group=in_group,
        payment_account_status=payment_account_status,
        currency_id=currency_id,
        handling_fee_config_id=handling_fee_config_id,
        group_type_ids=group_type_ids
    )
    return await telegram_account_handler.get_chat_groups(group_query=group_query)


@router.get(
    path="/group/{group_id}",
    response_model=GroupInfo,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_access_token)]
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
    return await telegram_account_handler.get_chat_group(group_id=group_id)


@router.put(
    path="/group/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_access_token)]
)
@inject
async def update_group(
    group_id: int,
    model: UpdateGroupInfo,
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param group_id:
    :param model:
    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.update_group(group_id=group_id, group_info=model)


@router.get(
    path="/group/{group_id}/members",
    response_model=GroupMembers,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_access_token)]
)
@inject
async def get_chat_group_members(
    group_id: int,
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param group_id:
    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.get_chat_group_members(group_id=group_id)
