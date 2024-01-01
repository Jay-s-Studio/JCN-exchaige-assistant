"""
Handling Fee API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query
from starlette import status

from app.containers import Container
from app.handlers.handing_fee import HandingFeeHandler
from app.libs.auth import check_all_authenticators
from app.serializers.v1.handing_fee import HandingFee
from app.routing import LogRouting

router = APIRouter(
    dependencies=[Depends(check_all_authenticators)],
    route_class=LogRouting
)


@router.get(
    path="/global",
    status_code=status.HTTP_200_OK
)
@inject
async def get_global_handing_fee(
    handing_fee_handler: HandingFeeHandler = Depends(Provide[Container.handing_fee_handler])
):
    """

    :param handing_fee_handler:
    :return:
    """
    return await handing_fee_handler.get_global_handing_fee()


@router.post(
    path="/global",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def set_global_handing_fee(
    model: HandingFee,
    handing_fee_handler: HandingFeeHandler = Depends(Provide[Container.handing_fee_handler])
):
    """

    :param model:
    :param handing_fee_handler:
    :return:
    """
    await handing_fee_handler.set_global_handing_fee(model=model)


@router.get(
    path="/{group_id}",
    status_code=status.HTTP_200_OK
)
@inject
async def get_handing_fee(
    group_id: str,
    handing_fee_handler: HandingFeeHandler = Depends(Provide[Container.handing_fee_handler])
):
    """

    :param group_id:
    :param handing_fee_handler:
    :return:
    """
    return await handing_fee_handler.get_handing_fee(group_id=group_id)


@router.post(
    path="/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def update_handing_fee(
    group_id: str,
    model: HandingFee,
    handing_fee_handler: HandingFeeHandler = Depends(Provide[Container.handing_fee_handler])
):
    """

    :param group_id:
    :param model:
    :param handing_fee_handler:
    :return:
    """
    return await handing_fee_handler.update_handing_fee(
        group_id=group_id,
        model=model
    )

