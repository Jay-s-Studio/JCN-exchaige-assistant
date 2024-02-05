"""
Schema for order
"""
from uuid import UUID

from pydantic import BaseModel, Field


class OrderCache(BaseModel):
    session_id: UUID = Field(description="Session ID")
    message_id: int = Field(description="Message ID")
    group_id: int = Field(description="Telegram Group ID")
    amount_to_exchange: float = Field(description="Amount")
    payment_currency: str = Field(description="Payment Currency")
    exchange_currency: str = Field(description="Exchange Currency")
    vendor_id: int = Field(description="Vendor ID")
    original_exchange_rate: float = Field(description="Original Exchange Rate")
    with_fee_exchange_rate: float = Field(description="With Fee Exchange Rate")
    total_amount: float = Field(description="Total Amount")
