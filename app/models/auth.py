"""
Models for auth
"""
from datetime import datetime

from pydantic import BaseModel


class JWTPayload(BaseModel):
    """
    JWT Payload
    """
    iss: str
    uid: str
    sub: str
    name: str
    iat: datetime
    exp: datetime
