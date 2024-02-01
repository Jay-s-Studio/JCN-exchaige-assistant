"""
Serializer for User API
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.mixins import UUIDBaseModel


class UserBase(UUIDBaseModel):
    """
    User
    """
    pass


class UserRegister(UUIDBaseModel):
    """
    New User
    """
    email: str = Field(description="Email")
    username: str = Field(description="Username")
    display_name: Optional[str] = Field(default=None, description="Display Name")
    password: str = Field(description="Password")
    confirm_password: str = Field(description="Confirm Password")


class UserLogin(BaseModel):
    """
    User Login
    """
    username: str
    password: str


class UserInfoResponse(UUIDBaseModel):
    """
    User Info Response
    """
    username: str
    display_name: str
    is_active: bool
    last_login: datetime


class TokenResponse(BaseModel):
    """
    Refresh Token Response
    """
    access_token: str
    token_type: str = "Bearer"


class LoginResponse(TokenResponse):
    """
    Login Response
    """
    pass
