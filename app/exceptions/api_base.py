"""
Exception for APIs
"""
from fastapi import HTTPException


class APIException(HTTPException):
    """APIException"""

    def __init__(
        self,
        status_code: int,
        message: str,
        **kwargs
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                **kwargs
            }
        )
