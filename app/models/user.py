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
    __table_args__ = {"schema": "public"}

    username = Column(sa.String(255), comment="Username")
    display_name = Column(sa.String(255), nullable=True, comment="Display Name")
    hash_password = Column(sa.String(255), comment="Hash Password")
    password_salt = Column(sa.String(255), comment="Password Salt")
    is_superuser = Column(sa.Boolean, nullable=False, server_default=sa.text('false'), comment="Is Superuser")
    is_active = Column(sa.Boolean, nullable=False, server_default=sa.text('false'), comment="Is Active")
    gac = Column(sa.String(16), comment='Google verification code secret_key')
    last_login_at = Column(sa.DateTime, comment='最登入时间')
