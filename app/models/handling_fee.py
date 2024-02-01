"""
Model for Handling Fee
"""
import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from app.libs.database.orm import ModelBase
from .mixins import AuditMixin, DeletedMixin, DescriptionMixin


class SysHandlingFeeConfig(ModelBase, AuditMixin, DeletedMixin, DescriptionMixin):
    """SysHandlingFeeConfig"""
    __tablename__ = "handling_fee_config"
    __table_args__ = {"schema": "public"}

    name = Column(sa.String(32), comment="Name")
    is_global = Column(sa.Boolean, server_default=sa.text("false"), comment="Is Global")


class SysHandlingFeeConfigItem(ModelBase, AuditMixin, DeletedMixin):
    """SysHandlingFeeConfigItem"""
    __tablename__ = "handling_fee_config_item"
    __table_args__ = (
        sa.UniqueConstraint("handling_fee_config_id", "currency_id", name="unique_handling_fee_config_item_key"),
        {"schema": "public"}
    )
    handling_fee_config_id = Column(
        UUID,
        sa.ForeignKey(
            column=SysHandlingFeeConfig.id,
            name="handling_fee_config_relation_id_fkey",
            ondelete="CASCADE",
        ),
        comment="Handling Fee Config ID"
    )
    currency_id = Column(
        UUID,
        sa.ForeignKey("public.currency.id", name="currency_id_fkey", ondelete="CASCADE"),
        comment="Currency ID"
    )
    buy_calculation_type = Column(sa.String(32), comment="Buy Calculation Type, Option: [addition|subtraction|multiplication|division]")
    buy_value = Column(sa.Float, comment="Buy Value")
    sell_calculation_type = Column(sa.String(32), comment="Sell Calculation Type, Option: [addition|subtraction|multiplication|division]")
    sell_value = Column(sa.Float, comment="Sell Value")
