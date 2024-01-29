"""
Authenticators for the app
"""
from fastapi import Depends

from app.exceptions.auth import UnauthorizedException
from app.libs.auth import BearerJWTAuth, APIKeyAuth
from app.libs.contexts.api_context import APIContext, set_api_context


async def check_all_authenticators(
    api_key_auth: APIContext = Depends(APIKeyAuth()),
    jwt_auth: APIContext = Depends(BearerJWTAuth())
) -> APIContext:
    """

    :param api_key_auth:
    :param jwt_auth:
    :return:
    """
    if not api_key_auth and not jwt_auth:
        raise UnauthorizedException()
    api_context = api_key_auth or jwt_auth
    set_api_context(api_context)
    return api_context
