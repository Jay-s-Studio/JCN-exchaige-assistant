"""
Auth Exception
"""
from starlette import status

from .api_base import APIException


class InvalidTokenException(APIException):
    """
    Invalid Token Exception
    """
    def __init__(self, message: str = None):
        if message is None:
            message = "Invalid authorization token"
        else:
            message = f"Invalid authorization token: {message}"
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message
        )


class UnauthorizedException(APIException):
    """
    Unauthorized Exception
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Unauthorized"
        )
