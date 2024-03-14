"""
Order API router
"""
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers import OrderHandler
from app.libs.depends import (
    check_access_token,
    DEFAULT_RATE_LIMITERS,
)
from app.route_classes import LogRoute
from app.serializers.v1.order import OrderList, UpdateOrder, OrderDetail

router = APIRouter(
    dependencies=[
        Depends(check_access_token),
        *DEFAULT_RATE_LIMITERS
    ],
    route_class=LogRoute
)


@router.get(
    path="/page",
    response_model=OrderList,
    status_code=status.HTTP_200_OK
)
@inject
async def get_order_page(
    page_index: int = 0,
    page_size: int = 10,
    order_handler: OrderHandler = Depends(Provide[Container.order_handler])
):
    """
    get order by pages
    :param page_index:
    :param page_size:
    :param order_handler:
    :return:
    """
    return await order_handler.get_order_page(
        page_index=page_index,
        page_size=page_size
    )


@router.get(
    path="/{order_id}",
    response_model=OrderDetail,
    status_code=status.HTTP_200_OK,
    response_model_exclude={"cart_id", "message_id"}
)
@inject
async def get_order_by_id(
    order_id: UUID,
    order_handler: OrderHandler = Depends(Provide[Container.order_handler])
):
    """
    get order by id
    :param order_id:
    :param order_handler:
    :return:
    """
    return await order_handler.get_order_by_id(order_id=order_id)


@router.put(
    path="/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def update_order_by_order_no(
    order_id: UUID,
    model: UpdateOrder,
    order_handler: OrderHandler = Depends(Provide[Container.order_handler])
):
    """
    update order by order no
    :param order_id:
    :param model:
    :param order_handler:
    :return:
    """
    await order_handler.update_order_description(
        order_id=order_id,
        description=model.description
    )
