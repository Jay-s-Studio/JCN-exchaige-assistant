"""
Serializers for Telegram Messages API
"""
from uuid import UUID

from pydantic import BaseModel, Field

from app.libs.consts.enums import PaymentAccountStatus, BotType


class TelegramBroadcast(BaseModel):
    """
    Telegram Broadcast
    """
    chat_id_list: list[int] = Field(description="Chat ID List")
    message: str = Field(description="Message", max_length=4096)
    type: BotType = Field(description="Bot Type")


class PaymentAccount(BaseModel):
    """
    Payment Account
    """
    order_id: UUID
    customer_id: int
    message: str
    message_id: int


class GroupPaymentAccountStatus(BaseModel):
    """
    Group Payment Account Status
    """
    status: PaymentAccountStatus


class OrderPaymentAccountStatus(GroupPaymentAccountStatus):
    """
    Order Payment Account Status
    """
    customer_id: int
    order_id: UUID
    status: PaymentAccountStatus


class ConfirmPay(BaseModel):
    """
    Confirm Pay
    """
    customer_id: int
    order_id: UUID
