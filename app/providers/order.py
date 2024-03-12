"""
OrderProvider
"""
from datetime import datetime
from uuid import UUID

import pytz
import sqlalchemy as sa
from redis.asyncio import Redis

from app.config import settings
from app.libs.database import Session, RedisPool
from app.libs.decorators.sentry_tracer import distributed_trace
from app.models import SysCart, SysOrder
from app.schemas.order import Order, Cart
from app.serializers.v1.order import OrderBase


class OrderProvider:
    """OrderProvider"""

    def __init__(
        self,
        session: Session,
        redis: RedisPool
    ):
        self._session = session
        self._redis: Redis = redis.create()

    @staticmethod
    def redis_name(name: str):
        """

        :return:
        """
        return f"{settings.APP_NAME}:{name}"

    @distributed_trace()
    async def get_order_page(
        self,
        page_index: int = 0,
        page_size: int = 10
    ) -> tuple[list[OrderBase], int]:
        """
        get order by pages
        :param page_index:
        :param page_size:
        :return:
        """
        try:
            result, count = await (
                self._session.select(
                    SysOrder.id,
                    SysOrder.order_no,
                    SysCart.payment_currency,
                    SysCart.payment_amount,
                    SysCart.exchange_currency,
                    SysCart.exchange_amount,
                    SysCart.original_exchange_rate,
                    SysCart.with_fee_exchange_rate,
                    SysCart.group_name,
                    SysCart.group_id,
                    SysCart.vendor_name,
                    SysCart.vendor_id,
                    SysCart.account_name,
                    SysCart.account_id,
                    SysOrder.status,
                    SysOrder.created_at,
                    SysOrder.description
                )
                .outerjoin(SysCart, SysOrder.cart_id == SysCart.id)
                .order_by(SysOrder.created_at.desc())
                .limit(page_size)
                .offset(page_index * page_size)
                .fetchpages(as_model=OrderBase)
            )
        except Exception as e:
            raise e
        else:
            return result, count
        finally:
            await self._session.close()

    @distributed_trace()
    async def get_order_by_id(
        self,
        order_id: UUID
    ) -> OrderBase:
        """
        get order by no
        :param order_id:
        :return:
        """
        try:
            order = await (
                self._session.select(
                    SysOrder.id,
                    SysOrder.order_no,
                    SysCart.payment_currency,
                    SysCart.payment_amount,
                    SysCart.exchange_currency,
                    SysCart.exchange_amount,
                    SysCart.original_exchange_rate,
                    SysCart.with_fee_exchange_rate,
                    SysCart.group_name,
                    SysCart.group_id,
                    SysCart.vendor_name,
                    SysCart.vendor_id,
                    SysCart.account_name,
                    SysCart.account_id,
                    SysOrder.status,
                    SysOrder.created_at,
                    SysOrder.description
                )
                .outerjoin(SysCart, SysOrder.cart_id == SysCart.id)
                .where(SysOrder.id == order_id)
                .fetchrow(as_model=OrderBase)
            )
        except Exception as e:
            raise e
        else:
            return order
        finally:
            await self._session.close()

    @distributed_trace()
    async def create_cart(self, cart: Cart) -> UUID:
        """
        create cart
        :param cart:
        :return:
        """
        cart_values = cart.model_dump()
        try:
            await (
                self._session.insert(SysCart)
                .values(**cart_values)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
            return cart.id
        finally:
            await self._session.close()

    @distributed_trace()
    async def generate_order_no(self) -> str:
        """
        generate order no
        :return:
        """
        today = datetime.now(tz=pytz.UTC).strftime('%Y%m%d')
        count = await (
            self._session.select(sa.func.count(SysOrder.id))
            .where(
                sa.and_(
                    SysOrder.created_at >= sa.func.CURRENT_DATE(),
                    SysOrder.created_at < sa.func.CURRENT_DATE() + sa.text("INTERVAL '1 day'")
                )
            )
            .fetchval()
        )
        count = int(count) + 1
        return f"O{today}{str(count).zfill(7)}"

    @distributed_trace()
    async def create_order(self, order: Order) -> str:
        """
        create order
        :param order:
        :return:
        """
        order_no = await self.generate_order_no()
        order.order_no = order_no
        order_values = order.model_dump()
        try:
            await (
                self._session.insert(SysOrder)
                .values(**order_values)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
            return order_no
        finally:
            await self._session.close()

    @distributed_trace()
    async def update_order_status(self, order_id: str, status: str) -> None:
        """
        update order status
        :param order_id:
        :param status:
        :return:
        """
        try:
            await (
                self._session.update(SysOrder)
                .values(status=status)
                .where(SysOrder.id == order_id)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()

    @distributed_trace()
    async def update_order_description(self, order_id: UUID, description: str) -> None:
        """
        update order description
        :param order_id:
        :param description:
        :return:
        """
        try:
            await (
                self._session.update(SysOrder)
                .values(description=description)
                .where(SysOrder.id == order_id)
                .execute()
            )
        except Exception as e:
            await self._session.rollback()
            raise e
        else:
            await self._session.commit()
        finally:
            await self._session.close()
