"""
Model for Message
"""
import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from app.libs.database.orm import ModelBase
from .telegram import SysTelegramChatGroup
from .mixins import AuditMixin, DeletedMixin


class SysMessage(ModelBase, AuditMixin, DeletedMixin):
    """SysMessage"""
    __tablename__ = "message"
    __table_args__ = {"schema": "public"}

    content = Column(sa.Text, comment="Content")
    type = Column(sa.String(16), comment="Type")


class SysMessageHistory(ModelBase, AuditMixin, DeletedMixin):
    """SysMessageHistory"""
    __tablename__ = "message_history"
    __table_args__ = (
        sa.UniqueConstraint(
            "message_id", "chat_group_id", name="unique_message_history_key"
        ),
        {"schema": "public"},
    )

    message_id = Column(
        UUID,
        sa.ForeignKey(
            column=SysMessage.id,
            name="message_history_relation_message_id_fkey",
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="Message ID",
    )
    chat_group_id = Column(
        sa.BigInteger,
        sa.ForeignKey(
            column=SysTelegramChatGroup.id,
            name="message_history_relation_chat_group_id_fkey",
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="Chat Group ID",
    )
    status = Column(sa.String(16), comment="Status")
    telegram_message_id = Column(sa.BigInteger, comment="Telegram Message ID")
    telegram_error_code = Column(sa.BigInteger, comment="Telegram Error Code")
    telegram_error_description = Column(sa.Text, comment="Telegram Error Description")
