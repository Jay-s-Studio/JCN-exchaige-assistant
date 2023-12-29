"""
API Context
"""
from contextvars import ContextVar, Token
from typing import Optional

from pydantic import BaseModel

auth_context = ContextVar("APIContext")


class APIContext(BaseModel):
    """API Context"""
    token: str
    api_key: Optional[str] = None
    user_id: str
    username: Optional[str] = None
    display_name: Optional[str] = None
    host: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None


def set_api_context(context: APIContext) -> Token:
    """

    :param context:
    :return:
    """
    return auth_context.set(context)


def get_api_context() -> APIContext:
    """

    :return:
    """
    return auth_context.get()
