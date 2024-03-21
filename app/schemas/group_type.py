"""
Schema for group type
"""
from uuid import UUID

from pydantic import Field, BaseModel


class GroupTypeRelation(BaseModel):
    """GroupTypeRelation"""
    chat_group_id: int = Field(title="Chat Group ID", description="Chat Group ID")
    chat_group_type_id: UUID = Field(title="Chat Group Type ID", description="Chat Group Type ID")
