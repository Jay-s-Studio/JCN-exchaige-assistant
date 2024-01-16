"""
Model for Gina
"""
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator

from app.libs.consts.enums import GinaIntention, GinaAction, Language


class GinaHeaders(BaseModel):
    """
    X-MessageChatGroupId:-1002050270240
    X-MessageChatUserId:1259597115
    X-MessageChatPlatform:telegram
    X-MessageChatMode:group
    X-MessageOS:mac
    X-MessageChatPlatformVersion:v1
    Content-Type:application/json;charset=utf8
    X-API-Key:jay
    GinaHeader
    """
    chat_group_id: str = Field(serialization_alias="X-MessageChatGroupId")
    chat_user_id: str = Field(serialization_alias="X-MessageChatUserId")
    chat_platform: str = Field(serialization_alias="X-MessageChatPlatform")
    chat_mode: str = Field(serialization_alias="X-MessageChatMode")
    os: str = Field(default="linux", serialization_alias="X-MessageOS")
    platform_version: str = Field(default="v1", serialization_alias="X-MessageChatPlatformVersion")
    content_type: str = Field(default="application/json;charset=utf8", serialization_alias="Content-Type")


class GinaMessage(BaseModel):
    """
    GinaMessage
    """
    text: str
    image: Optional[str] = None


class GinaPayload(BaseModel):
    """
    GinaPayload
    """
    messages: List[GinaMessage]


class GinaResponse(BaseModel):
    """
    GinaResponse
    """
    reply: str
    intention: Optional[GinaIntention] = Field(default=None)
    action: Optional[GinaAction] = Field(default=None)
    payment_currency: Optional[str] = Field(default=None, description="Payment Currency")
    exchange_currency: Optional[str] = Field(default=None, description="Exchange Currency")
    amount_to_exchange: Optional[float] = Field(default=None, description="Amount to Exchange")
    language: Optional[Language] = Field(default=Language.ZH_TW, description="Language")

    @field_validator("intention", mode="before")
    def check_intention(cls, value: str):
        """
        check intention
        :param value:
        :return:
        """
        try:
            return GinaIntention(value)
        except ValueError:
            return None

    @field_validator("action", mode="before")
    def check_action(cls, value: str):
        """
        check action
        :param value:
        :return:
        """
        try:
            return GinaAction(value)
        except ValueError:
            return None
