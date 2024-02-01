"""
Handling Fee API Router
"""
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers.handling_fee import HandlingFeeHandler
from app.libs.depends import check_all_authenticators, DEFAULT_RATE_LIMITERS
from app.route_classes import LogRoute
from app.serializers.v1.handling_fee import HandlingFeeConfig, HandlingFeeConfigPage

router = APIRouter(
    dependencies=[
        Depends(check_all_authenticators),
        *DEFAULT_RATE_LIMITERS
    ],
    route_class=LogRoute
)


@router.get(
    path="/configs",
    response_model=HandlingFeeConfigPage,
    status_code=status.HTTP_200_OK
)
@inject
async def get_handling_fee_config_page(
    page_index: int = 0,
    page_size: int = 10,
    handling_fee_handler: HandlingFeeHandler = Depends(Provide[Container.handling_fee_handler])
) -> HandlingFeeConfigPage:
    """
    Get handling fee config page
    """
    return await handling_fee_handler.get_handling_fee_config_page(page_index, page_size)


@router.get(
    path="/config/{config_id}",
    response_model=HandlingFeeConfig,
    status_code=status.HTTP_200_OK
)
@inject
async def get_handling_fee_config(
    config_id: UUID,
    handling_fee_handler: HandlingFeeHandler = Depends(Provide[Container.handling_fee_handler])
) -> HandlingFeeConfig:
    """
    Get handling fee config
    """
    return await handling_fee_handler.get_handling_fee_config(config_id)


@router.post(
    path="/config",
    status_code=status.HTTP_201_CREATED
)
@inject
async def create_handling_fee_config(
    config: HandlingFeeConfig,
    handling_fee_handler: HandlingFeeHandler = Depends(Provide[Container.handling_fee_handler])
):
    """
    Create handling fee config
    """
    await handling_fee_handler.create_handling_fee_config(config)
    return {"id": config.id}


@router.put(
    path="/config/{config_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def update_handling_fee_config(
    config_id: UUID,
    config: HandlingFeeConfig,
    handling_fee_handler: HandlingFeeHandler = Depends(Provide[Container.handling_fee_handler])
) -> None:
    """
    Update handling fee config
    """
    await handling_fee_handler.update_handling_fee_config(config_id=config_id, config=config)
