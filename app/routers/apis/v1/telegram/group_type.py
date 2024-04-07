"""
Telegram Group Type API Router
"""
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query
from starlette import status

from app.containers import Container
from app.handlers.telegram import TelegramGroupTypeHandler
from app.libs.depends import check_access_token, DEFAULT_RATE_LIMITERS
from app.route_classes import LogRoute
from app.schemas.mixins import UUIDBaseModel
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
    name: str = Query(default=None, description="Group type name"),
    telegram_group_type_handler: TelegramGroupTypeHandler = Depends(Provide[Container.telegram_group_type_handler])
):
    """
    Get group types
    """
    return await telegram_group_type_handler.get_group_types(name=name)


@router.post(
    path="/create",
    response_model=UUIDBaseModel,
    status_code=status.HTTP_201_CREATED
)
@inject
async def create_group_type(
    group_type: TelegramGroupType,
    telegram_group_type_handler: TelegramGroupTypeHandler = Depends(Provide[Container.telegram_group_type_handler])
) -> UUIDBaseModel:
    """
    Create a group type
    """
    return await telegram_group_type_handler.create_group_type(group_type=group_type)


@router.put(
    path="/{group_type_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def update_group_type(
    group_type_id: UUID,
    group_type: TelegramGroupType,
    telegram_group_type_handler: TelegramGroupTypeHandler = Depends(Provide[Container.telegram_group_type_handler])
):
    """
    Update a group type
    """
    group_type.id = group_type_id
    await telegram_group_type_handler.update_group_type(group_type=group_type)


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
