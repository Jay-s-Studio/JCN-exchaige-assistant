"""
Schema for order
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.libs.consts.enums import CartStatus, OrderStatus, Language
from .mixins import UUIDBaseModel


class Cart(UUIDBaseModel):
    """
    Cart
    """
    model_config = ConfigDict(use_enum_values=True)
    message_id: int = Field(description="Message ID")
    language: Language = Field(default=Language.ZH_TW, description="Language")
    group_name: str = Field(description="Group Name")
    group_id: int = Field(description="Group ID")
    vendor_name: str = Field(description="Vendor Name")
    vendor_id: int = Field(description="Vendor ID")
    account_name: str = Field(description="Account Name")
    account_id: int = Field(description="Account ID")
    payment_currency: str = Field(description="Payment Currency")
    payment_amount: float = Field(description="Payment Amount")
    exchange_currency: str = Field(description="Exchange Currency")
    original_exchange_rate: float = Field(description="Original Exchange Rate")
    with_fee_exchange_rate: float = Field(description="With Fee Exchange Rate")
    status: CartStatus = Field(default=CartStatus.PENDING, description="Status")


class Order(UUIDBaseModel):
    """
    Order
    """
    order_no: Optional[str] = Field(default=None, description="Order No")
    cart_id: UUID = Field(description="Cart ID")
    expiration_of_pay: Optional[datetime] = Field(default=None, description="Payment Time")
    status: OrderStatus = Field(default=OrderStatus.WAIT_FOR_PAYMENT_ACCOUNT, description="Status")
