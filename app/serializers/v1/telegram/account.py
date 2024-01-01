"""
Serializers for Telegram Account API
"""
from typing import Optional, List

from pydantic import BaseModel, Field

from app.libs.consts.enums import BotType


class TelegramAccount(BaseModel):
    """
    Telegram Account
    """
    id: str
    username: str
    first_name: str
    last_name: str
    is_bot: bool


class TelegramGroup(BaseModel):
    """
    Telegram Broadcast
    """
    id: int = Field(description="Group ID")
    title: str = Field(description="Group Title")
    description: Optional[str] = Field(default=None, description="Group Description")
    has_bot: bool = Field(description="Group Has Bot")
    bot_type: BotType = Field(description="Group Bot Type")


class GroupsResponse(BaseModel):
    """
    Groups Response
    """
    total: int = Field(default=0, description="Total Groups")
    groups: List[Optional[TelegramGroup]] = Field(default=[], description="Group List")


class VendorResponse(BaseModel):
    """
    Vendor Response
    """
    total: int = Field(default=0, description="Total Vendors")
    vendors: List[Optional[TelegramGroup]] = Field(default=[], description="Vendor List")


class CustomerResponse(BaseModel):
    """
    Customer Response
    """
    total: int = Field(default=0, description="Total Customers")
    customers: List[Optional[TelegramGroup]] = Field(default=[], description="Customer List")
