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
