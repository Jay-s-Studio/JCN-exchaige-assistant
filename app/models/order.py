"""
Model for order
"""
import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from app.libs.database.orm import ModelBase
from .telegram import SysTelegramAccount, SysTelegramChatGroup
from .mixins import AuditMixin, DeletedMixin, BaseMixin


class SysCart(ModelBase, AuditMixin, DeletedMixin):
    """SysCart"""
    __tablename__ = "cart"
    __table_args__ = {"schema": "public"}

    message_id = Column(sa.BigInteger, comment="Message ID")
    language = Column(sa.String(8), comment="Message language. Enum option refer to Language")
    group_name = Column(sa.String(255), comment="Group Name")
    group_id = Column(
        sa.BigInteger,
        sa.ForeignKey(
            SysTelegramChatGroup.id,
            name="group_id_fkey",
            ondelete="SET NULL"
        ),
        comment="Group ID"
    )
    vendor_name = Column(sa.String(255), comment="Vendor Name")
    vendor_id = Column(
        sa.BigInteger,
        sa.ForeignKey(
            SysTelegramChatGroup.id,
            name="vendor_id_fkey",
            ondelete="SET NULL"
        ),
        comment="Vendor ID"
    )
    account_name = Column(sa.String(255), comment="Account Name")
    account_id = Column(
        sa.BigInteger,
        sa.ForeignKey(
            SysTelegramAccount.id,
            name="account_id_fkey",
            ondelete="SET NULL"
        ),
        comment="Account ID"
    )
    payment_currency = Column(sa.String(8), comment="Payment Currency")
    payment_amount = Column(sa.Float, comment="Payment Amount")
    exchange_currency = Column(sa.String(8), comment="Exchange Currency")
    original_exchange_rate = Column(sa.Float, comment="Original Exchange Rate")
    with_fee_exchange_rate = Column(sa.Float, comment="With Fee Exchange Rate")
    status = Column(sa.String(64), nullable=False, comment="Status. Enum option refer to CartStatus")


class SysOrder(ModelBase, BaseMixin):
    """SysOrder"""
    __tablename__ = "order"
    __table_args__ = {"schema": "public"}

    order_no = Column(sa.String(32), index=True, comment="Order No")
    cart_id = Column(
        UUID,
        sa.ForeignKey(
            SysCart.id,
            name="cart_id_fkey",
            ondelete="SET NULL"
        ),
        nullable=False
    )
    expiration_of_pay = Column(sa.DateTime(timezone=True), comment="Expiration of Pay")
    status = Column(sa.String(64), comment="Order Status. Enum option refer to OrderStatus")
