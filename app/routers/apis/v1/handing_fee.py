"""
Handling Fee API Router
"""
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers.handing_fee import HandingFeeHandler
from app.libs.depends import check_all_authenticators, DEFAULT_RATE_LIMITERS
from app.route_classes import LogRoute
from app.serializers.v1.handing_fee import HandingFeeConfig, HandingFeeConfigPage

router = APIRouter(
    dependencies=[
        Depends(check_all_authenticators),
        *DEFAULT_RATE_LIMITERS
    ],
    route_class=LogRoute
)


@router.get(
    path="/configs",
    response_model=HandingFeeConfigPage,
    status_code=status.HTTP_200_OK
)
@inject
async def get_handing_fee_config_page(
    page_index: int = 0,
    page_size: int = 10,
    handing_fee_handler: HandingFeeHandler = Depends(Provide[Container.handing_fee_handler])
) -> HandingFeeConfigPage:
    """
    Get handing fee config page
    """
    return await handing_fee_handler.get_handing_fee_config_page(page_index, page_size)


@router.get(
    path="/config/{config_id}",
    response_model=HandingFeeConfig,
    status_code=status.HTTP_200_OK
)
@inject
async def get_handing_fee_config(
    config_id: UUID,
    handing_fee_handler: HandingFeeHandler = Depends(Provide[Container.handing_fee_handler])
) -> HandingFeeConfig:
    """
    Get handing fee config
    """
    return await handing_fee_handler.get_handing_fee_config(config_id)


@router.post(
    path="/config",
    status_code=status.HTTP_201_CREATED
)
@inject
async def create_handing_fee_config(
    config: HandingFeeConfig,
    handing_fee_handler: HandingFeeHandler = Depends(Provide[Container.handing_fee_handler])
):
    """
    Create handing fee config
    """
    await handing_fee_handler.create_handing_fee_config(config)
    return {"id": config.id}


@router.put(
    path="/config/{config_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def update_handing_fee_config(
    config_id: UUID,
    config: HandingFeeConfig,
    handing_fee_handler: HandingFeeHandler = Depends(Provide[Container.handing_fee_handler])
) -> None:
    """
    Update handing fee config
    """
    await handing_fee_handler.update_handing_fee_config(config_id=config_id, config=config)
