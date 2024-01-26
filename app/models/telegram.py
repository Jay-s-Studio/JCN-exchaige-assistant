"""
Model for Telegram
"""
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import Column

from app.libs.database.orm import Base
from .mixins import AuditMixin, DeletedMixin


class TelegramAccount(Base, AuditMixin, DeletedMixin):
    """TelegramAccount"""
    __tablename__ = "telegram_account"
    __table_args__ = {"schema": "public"}

    id = Column(sa.BigInteger, primary_key=True, comment="Account ID")
    username = Column(sa.String(255), nullable=True, comment="Username")
    first_name = Column(sa.String(255), nullable=True, comment="First Name")
    last_name = Column(sa.String(255), nullable=True, comment="Last Name")
    full_name = Column(sa.String(255), nullable=True, comment="Full Name")
    name = Column(sa.String(255), nullable=True, comment="Name")
    language_code = Column(sa.String(255), nullable=True, comment="Language Code")
    is_bot = Column(sa.Boolean, nullable=True, comment="Is Bot")
    is_premium = Column(sa.Boolean, nullable=True, comment="Is Premium")
    link = Column(sa.String(255), nullable=True, comment="Link")
    description = Column(sa.Text, nullable=True, comment="Description")
    join_at = Column(sa.DateTime, nullable=True, comment="Join At")


class TelegramChatGroup(Base, AuditMixin, DeletedMixin):
    """TelegramChatGroup"""
    __tablename__ = "telegram_chat_group"
    __table_args__ = {"schema": "public"}

    id = Column(sa.BigInteger, primary_key=True, comment="Chat Group ID")
    title = Column(sa.String(255), nullable=True, comment="Title")
    type = Column(sa.String(255), nullable=True, comment="Type")
    in_group = Column(sa.Boolean, nullable=True, comment="In Group")
    bot_type = Column(sa.String(255), nullable=True, comment="Bot Type")
    description = Column(sa.Text, nullable=True, comment="Description")
    default_currency = Column(sa.String(255), nullable=True, comment="Default Currency")
