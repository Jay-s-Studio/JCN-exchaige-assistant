"""
Serializer for User API
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.libs.consts.enums import StatusBase
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


class ChangePassword(BaseModel):
    """
    Change Password
    """
    old_password: str
    new_password: str
    confirm_password: str
    otp: Optional[str] = Field(default=None, description="OTP")


class TwoFactorVerify(BaseModel):
    """
    Two Factor Verify
    """
    otp: str


class UserInfoResponse(UUIDBaseModel):
    """
    User Info Response
    """
    username: str
    display_name: str
    is_active: bool
    last_login: datetime
    two_factor_status: StatusBase = Field(default=StatusBase.DISABLED, description="2FA Status")


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
    two_factor_status: StatusBase = Field(default=StatusBase.DISABLED, description="2FA Status")


class OTPInfo(BaseModel):
    """
    OTP Info
    """
    secret: str
    uri: str


class VerifyOTP(BaseModel):
    """
    Verify OTP
    """
    otp: str
