"""
Auth Exception
"""
from fastapi import HTTPException
from starlette import status


class InvalidAuthorizationToken(HTTPException):
    """
    Invalid Authorization Token Exception
    """
    def __init__(self, details=""):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authorization token: {details}"
        )
