"""
Serializers for Telegram Messages API
"""
from uuid import UUID

from pydantic import BaseModel

from app.libs.consts.enums import PaymentAccountStatus


class TelegramBroadcast(BaseModel):
    """
    Telegram Broadcast
    """
    chat_id: str
    message: str


class PaymentAccount(BaseModel):
    """
    Payment Account
    """
    session_id: UUID
    customer_id: int
    message: str


class GroupPaymentAccountStatus(BaseModel):
    """
    Group Payment Account Status
    """
    customer_id: int
    session_id: UUID
    status: PaymentAccountStatus


class ConfirmPay(BaseModel):
    """
    Confirm Pay
    """
    customer_id: int
    session_id: UUID
