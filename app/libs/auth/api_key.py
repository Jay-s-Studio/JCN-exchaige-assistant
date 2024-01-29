"""
API Key Auth
"""
from typing import Optional

from fastapi import Request
from fastapi.security import APIKeyHeader

from app.config import settings
from app.libs.contexts.api_context import APIContext


class APIKeyAuth(APIKeyHeader):
    """APIKeyAuth"""

    def __init__(self, name: str = "X-API-KEY"):
        super().__init__(name=name, auto_error=False)

    async def __call__(self, request: Request) -> Optional[APIContext]:
        if api_key := await super().__call__(request=request):
            return await self.check_key(request=request, key=api_key)
        return None

    @staticmethod
    async def check_key(
        request: Request,
        key: str
    ):
        """

        :param request:
        :param key:
        :return:
        """
        if key != settings.API_KEY:
            return None
        return APIContext(
            api_key=key,
            username="system",
            host=request.client.host,
            url=str(request.url),
            path=request.url.path
        )
