"""
Model for Gina
"""
from typing import Optional, List

from pydantic import BaseModel, Field


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
