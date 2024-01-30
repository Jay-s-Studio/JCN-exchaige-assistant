"""
Serializers for Telegram Account API
"""
from typing import Optional, List

from pydantic import BaseModel, Field

from app.libs.consts.enums import BotType
from app.schemas.account.telegram import TelegramAccount, TelegramChatGroup


class RawTelegramAccount(TelegramAccount):  # noqa
    pass


class RawTelegramGroup(TelegramChatGroup):
    pass


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


class TelegramGroup(BaseModel):
    """
    Telegram Broadcast
    """
    id: int = Field(description="Group ID")
    title: str = Field(description="Group Title")
    description: Optional[str] = Field(default=None, description="Group Description")
    in_group: bool = Field(description="Is In Group")
    bot_type: BotType = Field(description="Group Bot Type")
    customer_service: Optional[TelegramAccount] = Field(default=None, description="Group Customer Service")


class GroupsResponse(BaseModel):
    """
    Groups Response
    """
    total: int = Field(default=0, description="Total Groups")
    groups: List[TelegramGroup] = Field(default=[], description="Group List")


class VendorResponse(BaseModel):
    """
    Vendor Response
    """
    vendors: List[TelegramGroup] = Field(default=[], description="Vendor List")


class CustomerResponse(BaseModel):
    """
    Customer Response
    """
    customers: List[TelegramGroup] = Field(default=[], description="Customer List")


class GroupMembersResponse(BaseModel):
    """
    Group Members Response
    """
    members: List[Optional[TelegramAccount]] = Field(default=[], description="Group Member List")


class UpdateTelegramGroup(BaseModel):
    """
    Update Telegram Group
    """
    customer_service_id: int = Field(description="Group Customer Service ID")
    description: Optional[str] = Field(default=None, description="Group Description")
