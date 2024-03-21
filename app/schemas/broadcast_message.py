"""
Schema for message
"""
from typing import Optional
from uuid import UUID

from pydantic import Field, ConfigDict

from app.libs.consts.enums import BotType, MessageStatus
from .mixins import UUIDBaseModel


class BroadcastMessage(UUIDBaseModel):
    """Message"""
    model_config = ConfigDict(use_enum_values=True)
    content: str = Field(title="Content", description="Content")
    type: BotType = Field(title="Type", description="Type")


class BroadcastMessageHistory(UUIDBaseModel):
    """MessageHistory"""
    model_config = ConfigDict(use_enum_values=True)
    message_id: UUID = Field(title="Message ID", description="Message ID")
    chat_group_id: int = Field(title="Chat Group ID", description="Chat Group ID")
    status: Optional[MessageStatus] = Field(default=None, title="Status", description="Status")
    telegram_message_id: Optional[int] = Field(default=None, title="Telegram Message ID", description="Telegram Message ID")
    telegram_error_code: Optional[int] = Field(default=None, title="Telegram Error Code", description="Telegram Error Code")
    telegram_error_description: Optional[str] = Field(default=None, title="Telegram Error Description", description="Telegram Error Description")
