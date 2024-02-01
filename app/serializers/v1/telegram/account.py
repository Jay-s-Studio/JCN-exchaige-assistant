"""
Serializers for Telegram Account API
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from app.libs.consts.enums import BotType


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
    # telegram raw data
    id: int
    title: str
    type: str
    in_group: bool
    bot_type: BotType

    @field_serializer("bot_type")
    def serialize_enum(self, value: BotType, _info):
        """
        serialize enum
        :param value:
        :param _info:
        :return:
        """
        return value.value


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


class GroupInfo(BaseModel):
    """
    Group Info
    """
    id: int
    title: str
    in_group: bool
    bot_type: BotType
    description: str
    customer_service_ids: List[int]
    currency_symbol: str
    handling_fee_name: str


class GroupList(BaseModel):
    """
    Group List
    """
    total: int = Field(default=0)
    groups: List[GroupInfo] = Field(default=[])


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


class GroupMembers(BaseModel):
    """
    Group Members
    """
    total: int = Field(default=0, description="Total Members")
    members: List[GroupMember] = Field(default=[], description="Group Members")
