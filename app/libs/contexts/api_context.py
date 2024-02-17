"""
API Context
"""
from contextvars import ContextVar, Token
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.libs.consts.enums import TokenScope

auth_context = ContextVar("APIContext")


class APIContext(BaseModel):
    """API Context"""
    token: Optional[str] = None
    scope: Optional[TokenScope] = None
    api_key: Optional[str] = None
    user_id: Optional[UUID] = None
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
