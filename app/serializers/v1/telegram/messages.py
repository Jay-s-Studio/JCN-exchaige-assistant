"""
Serializers for Telegram Messages API
"""
from uuid import UUID

from pydantic import BaseModel


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
