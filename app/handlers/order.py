"""
OrderHandler
"""
from uuid import UUID

from app.libs.decorators.sentry_tracer import distributed_trace
from app.providers import OrderProvider
from app.serializers.v1.order import OrderDetail, OrderList


class OrderHandler:
    """OrderHandler"""

    def __init__(
        self,
        order_provider: OrderProvider
    ):
        self._order_provider = order_provider

    @distributed_trace()
    async def get_order_page(
        self,
        page_index: int = 0,
        page_size: int = 10
    ) -> OrderList:
        """
        get order by pages
        :param page_index:
        :param page_size:
        :return:
        """
        orders, total = await self._order_provider.get_order_page(
            page_index=page_index,
            page_size=page_size
        )
        return OrderList(orders=orders, total=total)

    @distributed_trace()
    async def get_order_by_id(self, order_id: UUID) -> OrderDetail:
        """
        get order by no
        :param order_id:
        :return:
        """
        order = await self._order_provider.get_order_by_id(order_id=order_id)
        return order

    @distributed_trace()
    async def update_order_description(
        self,
        order_id: UUID,
        description: str
    ):
        """
        update order description
        :param order_id:
        :param description:
        :return:
        """
        await self._order_provider.update_order_description(
            order_id=order_id,
            description=description
        )

