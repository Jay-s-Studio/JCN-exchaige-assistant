"""
Model for Telegram
"""
import sqlalchemy as sa
from sqlalchemy import Column

from app.libs.database.orm import Base, ModelBase
from .mixins import AuditMixin, DeletedMixin, DescriptionMixin


class SysTelegramAccount(Base, AuditMixin, DeletedMixin, DescriptionMixin):
    """SysTelegramAccount"""
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


class SysTelegramChatGroup(Base, AuditMixin, DeletedMixin, DescriptionMixin):
    """SysTelegramChatGroup"""
    __tablename__ = "telegram_chat_group"
    __table_args__ = {"schema": "public"}

    id = Column(sa.BigInteger, primary_key=True, comment="Chat Group ID")
    title = Column(sa.String(255), nullable=True, comment="Title")
    type = Column(sa.String(255), nullable=True, comment="Type")
    in_group = Column(sa.Boolean, nullable=True, comment="In Group")
    bot_type = Column(sa.String(255), nullable=True, comment="Bot Type")
    # default_currency = Column(sa.String(255), nullable=True, comment="Default Currency")


class SysTelegramAccountGroupRelation(ModelBase):
    """SysTelegramAccountGroupRelation"""
    __tablename__ = "telegram_account_group_relation"
    __table_args__ = (
        sa.UniqueConstraint('account_id', 'chat_group_id', name='unique_telegram_account_group_relation_uc'),
        {"schema": "public"}
    )
    account_id = Column(
        sa.BigInteger,
        sa.ForeignKey(
            column=SysTelegramAccount.id,
            name="telegram_account_relation_account_id_fkey",
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="Account ID",
    )
    chat_group_id = Column(
        sa.BigInteger,
        sa.ForeignKey(
            column=SysTelegramChatGroup.id,
            name="telegram_account_relation_chat_group_id_fkey",
            ondelete="CASCADE",
        ),
        nullable=False,
        comment="Chat Group ID",
    )