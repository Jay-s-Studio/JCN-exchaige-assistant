"""
Model for User
"""
import sqlalchemy as sa
from sqlalchemy import Column

from app.libs.database.orm import ModelBase
from .mixins import AuditMixin, DeletedMixin


class User(ModelBase, AuditMixin, DeletedMixin):
    """User"""
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}

    username = Column(sa.String(255), comment="Username")
    display_name = Column(sa.String(255), nullable=True, comment="Display Name")
    hash_password = Column(sa.String(255), comment="Hash Password")
    password_salt = Column(sa.String(255), comment="Password Salt")
    is_active = Column(sa.Boolean, comment="Is Active")
    last_login = Column(sa.DateTime, nullable=True, comment="Last Login")
