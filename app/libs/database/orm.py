import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ModelBase(Base):
    """ModelBase"""
    __abstract__ = True
    id = Column(UUID, server_default=sa.text("gen_random_uuid()"), primary_key=True, comment="Primary Key")

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        return None
