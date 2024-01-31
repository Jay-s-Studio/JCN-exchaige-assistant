"""
Model for Handing Fee
"""
import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from app.libs.database.orm import ModelBase
from .mixins import AuditMixin, DeletedMixin, DescriptionMixin


class SysHandingFeeConfig(ModelBase, AuditMixin, DeletedMixin, DescriptionMixin):
    """SysHandingFeeConfig"""
    __tablename__ = "handing_fee_config"
    __table_args__ = {"schema": "public"}

    name = Column(sa.String(255), comment="Name")
    is_global = Column(sa.Boolean, server_default=sa.text("false"), comment="Is Global")


class SysHandingFeeConfigItem(ModelBase, AuditMixin, DeletedMixin):
    """SysHandingFeeConfigItem"""
    __tablename__ = "handing_fee_config_item"
    __table_args__ = (
        sa.UniqueConstraint("handing_fee_config_id", "currency_id", name="unique_handing_fee_config_item_uc"),
        {"schema": "public"}
    )
    handing_fee_config_id = Column(
        UUID,
        sa.ForeignKey(
            column=SysHandingFeeConfig.id,
            name="handing_fee_config_relation_id_fkey",
            ondelete="CASCADE",
        ),
        comment="Handing Fee Config ID"
    )
    currency_id = Column(
        UUID,
        sa.ForeignKey("public.currency.id", name="currency_id_fkey", ondelete="CASCADE"),
        comment="Currency ID"
    )
    calculation_type = Column(sa.String(32), comment="Calculation Type")
    value = Column(sa.Float, comment="Value")
