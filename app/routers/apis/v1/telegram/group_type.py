"""
Telegram Group Type API Router
"""
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers.telegram import TelegramGroupTypeHandler
from app.libs.depends import check_access_token, DEFAULT_RATE_LIMITERS
from app.route_classes import LogRoute
from app.serializers.v1.telegram import (
    TelegramGroupType,
    TelegramGroupTypes,
)

router = APIRouter(
    dependencies=[
        Depends(check_access_token),
        *DEFAULT_RATE_LIMITERS
    ],
    route_class=LogRoute
)


@router.get(
    path="/list",
    response_model=TelegramGroupTypes,
)
@inject
async def get_group_types(
    telegram_group_type_handler: TelegramGroupTypeHandler = Depends(Provide[Container.telegram_group_type_handler])
):
    """
    Get group types
    """
    return await telegram_group_type_handler.get_group_types()


@router.post(
    path="/",
    response_model=TelegramGroupType,
    status_code=status.HTTP_201_CREATED
)
@inject
async def create_group_type(
    group_type: TelegramGroupType,
    telegram_group_type_handler: TelegramGroupTypeHandler = Depends(Provide[Container.telegram_group_type_handler])
) -> TelegramGroupType:
    """
    Create a group type
    """
    return await telegram_group_type_handler.create_group_type(group_type=group_type)


@router.put(
    path="/{group_type_id}",
    response_model=TelegramGroupType,
    status_code=status.HTTP_200_OK
)
@inject
async def update_group_type(
    group_type_id: UUID,
    group_type: TelegramGroupType,
    telegram_group_type_handler: TelegramGroupTypeHandler = Depends(Provide[Container.telegram_group_type_handler])
) -> TelegramGroupType:
    """
    Update a group type
    """
    group_type.id = group_type_id
    return await telegram_group_type_handler.update_group_type(group_type=group_type)


@router.delete(
    path="/{group_type_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_group_type(
    group_type_id: UUID,
    telegram_group_type_handler: TelegramGroupTypeHandler = Depends(Provide[Container.telegram_group_type_handler])
) -> None:
    """
    Delete a group type
    """
    await telegram_group_type_handler.delete_group_type(group_type_id=group_type_id)
