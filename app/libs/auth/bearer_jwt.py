"""
Bearer token authentication
"""
from typing import Optional

from fastapi import Request
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

from app.handlers import AuthHandler
from app.libs.contexts.api_context import APIContext


class BearerJWTAuth(HTTPBearer):
    """BearerJWTAuth"""

    def __init__(self) -> None:
        super().__init__(auto_error=False)

    async def __call__(self, request: Request) -> Optional[APIContext]:
        result: Optional[HTTPAuthorizationCredentials] = await super().__call__(
            request=request
        )
        if not result:
            return None
        api_context = await self.authenticate(request=request, token=result.credentials)
        return api_context

    @staticmethod
    async def authenticate(request: Request, token):
        """

        :param request:
        :param token:
        :return:
        """
        auth_handler = AuthHandler()
        token_info = auth_handler.verify_token(token=token)
        return APIContext(
            token=token,
            user_id=token_info.uid,
            username=token_info.sub,
            display_name=token_info.name,
            host=request.client.host,
            url=str(request.url),
            path=request.url.path
        )
