"""
Models for Telegram account
"""
from typing import Optional

from pydantic import BaseModel


class TelegramAccount(BaseModel):
    """
    TelegramAccount
    """
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    language_code: Optional[str]
    is_bot: bool
    is_premium: bool = False
