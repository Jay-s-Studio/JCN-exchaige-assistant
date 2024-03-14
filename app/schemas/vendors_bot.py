"""
Schema for vendors bot
"""
from uuid import UUID

from pydantic import BaseModel, field_serializer


class PaymentAccount(BaseModel):
    """
    Telegram Flow Chat
    """
    order_id: UUID
    customer_id: int
    vendor_id: int
    payment_currency: str
    exchange_currency: str
    total_amount: float

    @field_serializer("order_id")
    def serialize_uuid(self, value: UUID, _info) -> str:
        """

        :param value:
        :param _info:
        :return:
        """
        return str(value)


class CheckReceipt(BaseModel):
    """
    Check Receipt
    """
    order_id: UUID
    customer_id: int
    vendor_id: int
    file_id: str
    file_name: str

    @field_serializer("order_id")
    def serialize_uuid(self, value: UUID, _info) -> str:
        """

        :param value:
        :param _info:
        :return:
        """
        return str(value)
