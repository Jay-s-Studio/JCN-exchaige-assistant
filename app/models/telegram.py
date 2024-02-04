"""
Model for Telegram
"""
import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from app.libs.database.orm import Base, ModelBase
from .handling_fee import SysHandlingFeeConfig
from .mixins import AuditMixin, DeletedMixin, DescriptionMixin
from ..libs.consts.enums import PaymentAccountStatus


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
    payment_account_status = Column(
        sa.String(32),
        nullable=True,
        comment="Payment Account Status. Options: ['preparing', 'out_of_stock']"
    )
    currency_id = Column(
        UUID,
        sa.ForeignKey("public.currency.id", name="currency_id_fkey", ondelete="SET NULL"),
        nullable=True,
        comment="Currency ID"
    )
    handling_fee_config_id = Column(
        UUID,
        sa.ForeignKey(
            column=SysHandlingFeeConfig.id,
            name="handling_fee_config_relation_id_fkey",
            ondelete="SET NULL",
        ),
        nullable=True,
        comment="Handling Fee Config ID"
    )


class SysTelegramChatGroupMember(ModelBase, AuditMixin, DeletedMixin):
    """SysTelegramChatGroupMember"""
    __tablename__ = "telegram_chat_group_member"
    __table_args__ = (
        sa.UniqueConstraint("account_id", "chat_group_id", name="unique_telegram_chat_group_member_key"),
        {"schema": "public"}
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
    is_customer_service = Column(sa.Boolean, server_default=sa.text("false"), comment="Is Customer Service")
