"""
审计信息
"""
import sqlalchemy as sa

from datetime import datetime
from sqlalchemy import Column, DateTime, String, text, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from .context import get_current_id, get_current_username

__all__ = [
    "DeletedMixin",
    "RemarkMixin",
    "OrderableMixin",
    "AuditCreatedAtMixin",
    "AuditCreatedByMixin",
    "AuditCreatedMixin",
    "AuditMixin",
    "AuditUpdatedMixin"
]


class AuditCreatedAtMixin(object):
    """AuditCreatedAtMixin"""

    @declared_attr
    def created_at(self):
        return Column(
            DateTime,
            server_default=sa.func.now,
            comment="Create Date",
            nullable=False
        )


class AuditCreatedByMixin(object):
    @declared_attr
    def created_by(self):
        return Column(
            String(64),
            default=get_current_username,
            comment="Create User Name",
            nullable=False
        )


class AuditCreatedMixin(AuditCreatedAtMixin, AuditCreatedByMixin):
    @declared_attr
    def created_by_id(self):
        return Column(UUID, default=get_current_id, comment="Create User ID")


class AuditUpdatedMixin(object):

    @declared_attr
    def updated_at(self):
        return Column(
            DateTime, server_default=sa.func.now(),
            onupdate=datetime.now,
            comment="Update Date",
            nullable=False
        )

    @declared_attr
    def updated_by_id(self):
        return Column(UUID, default=get_current_id, onupdate=get_current_id, comment="Update User ID")

    @declared_attr
    def updated_by(self):
        return Column(
            String(32),
            default=get_current_username,
            onupdate=get_current_username,
            comment="Update User Name",
            nullable=False
        )


class AuditMixin(object):

    @declared_attr
    def created_at(self):
        return Column(
            DateTime,
            server_default=sa.func.now(),
            comment="Create Date",
            nullable=False
        )

    @declared_attr
    def updated_at(self):
        return Column(
            DateTime,
            server_default=sa.func.now(),
            onupdate=datetime.now,
            comment="Update Date",
            nullable=False
        )

    @declared_attr
    def created_by_id(self):
        return Column(UUID, default=get_current_id, comment="Create User ID")

    @declared_attr
    def updated_by_id(self):
        return Column(UUID, default=get_current_id, onupdate=get_current_id, comment="Update User ID")

    @declared_attr
    def created_by(self):
        return Column(
            String(32),
            default=get_current_username,
            comment="Create User Name",
            nullable=False
        )

    @declared_attr
    def updated_by(self):
        return Column(
            String(32),
            default=get_current_username,
            onupdate=get_current_username,
            comment="Update User Name",
            nullable=False
        )


class OrderableMixin(object):

    @declared_attr
    def sequence(self):
        return Column(
            Float,
            server_default=text("extract(epoch from now())"),
            comment="Display order, small to large, positive order, default value current timestamp"
        )


class DeletedMixin(object):

    @declared_attr
    def delete_reason(self):
        return Column(String(64), comment="Delete Reason")

    @declared_attr
    def is_deleted(self):
        return Column(
            Boolean,
            server_default=text("false"),
            comment="Is Deleted(Logical Delete)",
            nullable=False
        )


class RemarkMixin(object):

    @declared_attr
    def remark(self):
        return Column(String(256), comment="Remark")
