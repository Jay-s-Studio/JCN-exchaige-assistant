"""
Model for Exchange Rate
"""
import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from app.libs.database.orm import ModelBase
from .mixins import AuditMixin


class SysExchangeRate(ModelBase, AuditMixin):
    """SysExchangeRate"""
    __tablename__ = "exchange_rate"
    __table_args__ = (
        sa.UniqueConstraint("telegram_chat_group_id", "currency_id", name="exchange_rate_telegram_chat_group_id_currency_id_key"),
        {"schema": "public"}
    )

    telegram_chat_group_id = Column(
        sa.BigInteger,
        sa.ForeignKey(
            column="public.telegram_chat_group.id",
            name="exchange_rate_telegram_chat_group_id_fkey",
            ondelete="CASCADE"
        ),
        nullable=False,
        comment="Telegram Chat Group ID"
    )
    currency_id = Column(
        UUID,
        sa.ForeignKey(
            column="public.currency.id",
            name="exchange_rate_currency_id_fkey",
            ondelete="CASCADE"
        ),
        nullable=False,
        comment="Currency ID"
    )
    buy_rate = Column(sa.Float, comment="Buy Rate")
    sell_rate = Column(sa.Float, comment="Sell Rate")
