"""
Model for User
"""
import sqlalchemy as sa
from sqlalchemy import Column

from app.libs.database.orm import ModelBase
from .mixins import AuditMixin, DeletedMixin


class SysUser(ModelBase, AuditMixin, DeletedMixin):
    """SysUser"""
    __tablename__ = "user"
    __table_args__ = (
        sa.UniqueConstraint("email", name="user_email_key"),
        {"schema": "public"}
    )

    email = Column(sa.String(255), comment="Email")
    username = Column(sa.String(255), comment="Username")
    display_name = Column(sa.String(255), nullable=True, comment="Display Name")
    hash_password = Column(sa.String(255), comment="Hash Password")
    password_salt = Column(sa.String(255), comment="Password Salt")
    is_superuser = Column(sa.Boolean, nullable=False, server_default=sa.text('false'), comment="Is Superuser")
    is_active = Column(sa.Boolean, nullable=False, server_default=sa.text('false'), comment="Is Active")
    otp_active = Column(sa.Boolean, nullable=False, server_default=sa.text('false'), comment="OTP Active")
    otp_secret = Column(sa.String(32), comment="OTP Secret")
    last_login_at = Column(sa.DateTime(timezone=True), comment="Last Login At")
