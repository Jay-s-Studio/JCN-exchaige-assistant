"""
Schema for vendors bot
"""
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_serializer, Field


class VendorBotBroadcast(BaseModel):
    """
    Vendor Bot Broadcast
    """
    chat_id: int
    message: str


class VendorBotChat(BaseModel):
    """
    Vendor Bot Chat
    """
    id: Optional[int] = Field(default=None, description="ID of the chat")
    type: Optional[str] = Field(default=None, description="Type of the chat, e.g. 'group', 'private', 'supergroup'")
    title: Optional[str] = Field(default=None, description="Title of the chat")
    all_members_are_administrators: Optional[bool] = Field(default=None, description="Whether all members of the chat are administrators")


class VendorBotFrom(BaseModel):
    """
    Vendor Bot From
    """
    id: Optional[int] = Field(default=None, description="ID of the user")
    is_bot: Optional[bool] = Field(default=None, description="Whether the user is a bot")
    username: Optional[str] = Field(default=None, description="Username of the user")
    first_name: Optional[str] = Field(default=None, description="First name of the user")


class VendorBotMessage(BaseModel):
    """
    Vendor Bot Message
    """
    message_id: int
    chat: Optional[VendorBotChat] = Field(default=None, description="Chat the message belongs to")
    text: Optional[str] = Field(default=None, description="Text of the message")
    group_chat_created: Optional[bool] = Field(default=None, description="Whether the group chat was created")
    date: Optional[int] = Field(default=None, description="Date the message was sent")
    from_: Optional[VendorBotFrom] = Field(default=None, alias="from", description="Sender of the message")


class GetPaymentAccount(BaseModel):
    """
    Get Payment Account
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


class ConfirmPayment(BaseModel):
    """
    Confirm Payment
    """
    order_id: UUID
    customer_id: int
    vendor_id: int
    message_id: int

    @field_serializer("order_id")
    def serialize_uuid(self, value: UUID, _info) -> str:
        """

        :param value:
        :param _info:
        :return:
        """
        return str(value)
