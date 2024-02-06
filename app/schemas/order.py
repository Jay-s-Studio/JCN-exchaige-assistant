"""
Schema for order
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.libs.consts.enums import OrderStatus, Language


class OrderCache(BaseModel):
    session_id: UUID = Field(description="Session ID")
    language: Optional[Language] = Field(default=Language.ZH_TW, description="Language")
    message_id: int = Field(description="Message ID")
    group_id: int = Field(description="Telegram Group ID")
    amount_to_exchange: float = Field(description="Amount")
    payment_currency: str = Field(description="Payment Currency")
    exchange_currency: str = Field(description="Exchange Currency")
    vendor_id: int = Field(description="Vendor ID")
    original_exchange_rate: float = Field(description="Original Exchange Rate")
    with_fee_exchange_rate: float = Field(description="With Fee Exchange Rate")
    total_amount: float = Field(description="Total Amount")
    payment_account: Optional[str] = Field(default=None, description="Payment Account")
    expiration_of_pay: Optional[datetime] = Field(default=None, description="Payment Time")
    status: OrderStatus = Field(default=OrderStatus.WAIT_FOR_PAYMENT_ACCOUNT, description="Status")
