"""
Serializers for Telegram Account API
"""
import json
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict

from app.libs.consts.enums import BotType, PaymentAccountStatus
from app.libs.shared import validator


class TelegramAccount(BaseModel):
    """TelegramAccount"""
    id: int
    username: Optional[str] = Field(default=None, description="Username")
    first_name: Optional[str] = Field(default=None, description="First Name")
    last_name: Optional[str] = Field(default=None, description="Last Name")
    full_name: Optional[str] = Field(default=None, description="Full Name")
    name: Optional[str] = Field(default=None, description="Name")
    language_code: Optional[str] = Field(default=None, description="Language Code")
    is_bot: bool = Field(default=False, description="Is Bot")
    is_premium: bool = False
    link: Optional[str] = Field(default=None, description="Link")


class TelegramChatGroup(BaseModel):
    """TelegramChatGroup"""
    model_config = ConfigDict(use_enum_values=True)
    id: int
    title: str
    type: str
    in_group: bool
    bot_type: BotType
    payment_account_status: Optional[PaymentAccountStatus] = Field(default=None, description="Payment Account Status")


class GroupMemberBase(BaseModel):
    """
    Group Member
    """
    account_id: int = Field(description="Account ID")
    chat_group_id: int = Field(description="Group ID")


class InitGroupMember(GroupMemberBase):
    """
    Init Group Member
    """
    is_customer_service: bool = Field(default=False, description="Is Customer Service")


class VendorResponse(BaseModel):
    """
    Vendor Response
    """
    vendors: List[TelegramChatGroup] = Field(default=[], description="Vendor List")


class GroupMember(BaseModel):
    """
    Group Member
    """
    id: int
    username: Optional[str] = Field(default=None, description="Username")
    first_name: Optional[str] = Field(default=None, description="First Name")
    last_name: Optional[str] = Field(default=None, description="Last Name")
    full_name: Optional[str] = Field(default=None, description="Full Name")
    name: Optional[str] = Field(default=None, description="Name")
    is_customer_service: Optional[bool] = Field(default=False, description="Is Customer Service")


class GroupMembers(BaseModel):
    """
    Group Members
    """
    total: int = Field(default=0, description="Total Members")
    members: List[GroupMember] = Field(default=[], description="Group Members")


class GroupInfo(BaseModel):
    """
    Group Info
    """
    id: int
    title: str
    in_group: bool
    bot_type: BotType
    description: Optional[str] = Field(default=None)
    payment_account_status: Optional[PaymentAccountStatus] = Field(default=None)
    customer_services: List[GroupMember] = Field(default=[])
    currency_symbol: Optional[str] = Field(default=None)
    handling_fee_name: Optional[str] = Field(default=None)

    @field_validator("customer_services", mode="before")
    def validate_customer_services(cls, value: List[str]):
        """
        Validate customer services
        :param value:
        :return:
        """
        if validator.is_empty(value):
            return []
        return [json.loads(item) for item in value]


class GroupList(BaseModel):
    """
    Group List
    """
    total: int = Field(default=0)
    groups: List[GroupInfo] = Field(default=[])


class UpdateGroupInfo(BaseModel):
    """
    Update Group Info
    """
    description: Optional[str] = Field(default=None, description="Description")
    customer_service_ids: Optional[List[int]] = Field(default=None, description="Customer Service IDs")
    currency_id: Optional[UUID] = Field(default=None, description="Currency ID")
    handling_fee_config_id: Optional[UUID] = Field(default=None, description="Handling Fee Config ID")

    @field_validator("currency_id", "handling_fee_config_id", mode="before")
    def validate_name(cls, value: str):
        """
        Validate name
        :param value:
        :return:
        """
        if validator.is_empty(value):
            return None
        return value
