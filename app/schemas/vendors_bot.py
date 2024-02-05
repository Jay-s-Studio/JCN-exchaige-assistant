"""
Schema for vendors bot
"""
from uuid import UUID

from pydantic import BaseModel, field_serializer


class PaymentAccount(BaseModel):
    """
    Telegram Flow Chat
    """
    session_id: UUID
    customer_id: int
    group_id: int
    payment_currency: str
    exchange_currency: str
    total_amount: float

    @field_serializer("session_id")
    def serialize_uuid(self, value: UUID, _info) -> str:
        """

        :param value:
        :param _info:
        :return:
        """
        return str(value)
