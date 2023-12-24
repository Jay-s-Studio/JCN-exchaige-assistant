"""
Serializer for User API
"""
from pydantic import BaseModel


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


class LoginResponse(BaseModel):
    """
    Login Response
    """

    access_token: str
    token_type: str = "Bearer"
