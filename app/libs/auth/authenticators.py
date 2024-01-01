"""
Authenticators for the app
"""
from fastapi import Depends

from .bearer_jwt import BearerJWTAuth
from app.libs.contexts.api_context import APIContext, set_api_context


async def check_all_authenticators(
    jwt_auth: APIContext = Depends(BearerJWTAuth()),
) -> APIContext:
    """

    :param jwt_auth:
    :return:
    """
    api_context = jwt_auth
    set_api_context(api_context)
    return api_context
