"""
Serializer for User API
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.mixins import UUIDBaseModel


class UserRegister(BaseModel):
    """
    New User
    """
    username: str
    password: str


class UserLogin(BaseModel):
    """
    User Login
    """
    username: str
    password: str


class TokenResponse(BaseModel):
    """
    Refresh Token Response
    """
    access_token: str
    token_type: str = "Bearer"


class LoginResponse(UUIDBaseModel, TokenResponse):
    """
    Login Response
    """
    username: str
    display_name: str
    is_active: bool
    last_login: datetime


class RefreshToken(BaseModel):
    """
    Refresh Token
    """
    user_id: UUID
