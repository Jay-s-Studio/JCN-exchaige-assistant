"""
Two factor token authentication
"""
from typing import Optional

from fastapi import Request

from app.handlers import AuthHandler
from app.libs.consts.enums import TokenScope
from app.libs.contexts.api_context import APIContext
from .access_token import AccessTokenAuth


class TwoFactorTokenAuth(AccessTokenAuth):
    """TwoFactorTokenAuth"""

    @staticmethod
    async def authenticate(request: Request, token) -> Optional[APIContext]:
        """

        :param request:
        :param token:
        :return:
        """
        auth_handler = AuthHandler()
        token_info = auth_handler.verify_token(token=token)
        if token_info.scope != TokenScope.TWO_FACTOR_AUTH:
            return None
        return APIContext(
            token=token,
            scope=token_info.scope,
            user_id=token_info.uid,
            username=token_info.sub,
            display_name=token_info.name,
            host=request.client.host,
            url=str(request.url),
            path=request.url.path
        )
