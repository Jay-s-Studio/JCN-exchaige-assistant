"""
Model for currency
"""
import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from app.libs.consts.enums import CurrencyType
from app.libs.database.orm import ModelBase
from .mixins import AuditMixin, DeletedMixin, DescriptionMixin, SortableMixin


class SysCurrency(ModelBase, AuditMixin, DeletedMixin, DescriptionMixin, SortableMixin):
    """SysTelegramAccount"""
    __tablename__ = "currency"
    __table_args__ = {"schema": "public"}

    symbol = Column(sa.String(16), nullable=False, comment="Symbol")
    type = Column(
        sa.String(32),
        server_default=sa.literal(CurrencyType.GENERAL.value),
        nullable=False,
        comment="Type"
    )
    path = Column(sa.String(128), nullable=False, comment="Path(Up to two levels), e.g. currency.id/currency.id")
    parent_id = Column(
        UUID,
        sa.ForeignKey("public.currency.id", name="currency_id_fkey", ondelete="CASCADE"),
        nullable=True,
        comment="Parent ID"
    )
