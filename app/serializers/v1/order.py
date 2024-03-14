"""
Serializers for order API
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.libs.consts.enums import OrderStatus
from app.schemas.mixins import UUIDBaseModel


class OrderBase(UUIDBaseModel):
    """
    OrderBase
    """
    order_no: str = Field(description="Order No")


class OrderDetail(OrderBase):
    """
    OrderDetail
    """
    cart_id: UUID = Field(description="Cart ID")
    payment_currency: str = Field(description="Payment Currency")
    payment_amount: float = Field(description="Payment Amount")
    exchange_currency: str = Field(description="Exchange Currency")
    exchange_amount: float = Field(description="Exchange Amount")
    original_exchange_rate: float = Field(description="Original Exchange Rate")
    with_fee_exchange_rate: float = Field(description="With Fee Exchange Rate")
    message_id: Optional[int] = Field(description="Message ID")
    group_name: str = Field(description="Order Group Name")
    group_id: int = Field(description="Order Group ID")
    vendor_name: str = Field(description="Vendor Name")
    vendor_id: int = Field(description="Vendor ID")
    account_name: str = Field(description="Order Account Name")
    account_id: int = Field(description="Order Account ID")
    status: OrderStatus = Field(description="Status")
    created_at: Optional[datetime] = Field(description="Created At")
    description: Optional[str] = Field(description="Description")


class OrderList(BaseModel):
    """
    OrderList
    """
    orders: list[OrderDetail]
    total: int


class UpdateOrder(BaseModel):
    """
    UpdateOrder
    """
    description: Optional[str] = Field(default=None, description="Description")
