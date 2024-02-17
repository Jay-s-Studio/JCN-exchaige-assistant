"""
Authenticators for the app
"""
from fastapi import Depends

from app.exceptions.auth import UnauthorizedException
from app.libs.auth import AccessTokenAuth, APIKeyAuth, TwoFactorTokenAuth
from app.libs.contexts.api_context import APIContext, set_api_context


async def check_all_authenticators(
    api_key_auth: APIContext = Depends(APIKeyAuth()),
    access_token: APIContext = Depends(AccessTokenAuth())
) -> APIContext:
    """

    :param api_key_auth:
    :param access_token:
    :return:
    """
    if not api_key_auth and not access_token:
        raise UnauthorizedException()
    api_context = api_key_auth or access_token
    set_api_context(api_context)
    return api_context


async def check_api_key_authenticator(
    api_key_auth: APIContext = Depends(APIKeyAuth())
) -> APIContext:
    """

    :param api_key_auth:
    :return:
    """
    if not api_key_auth:
        raise UnauthorizedException()
    set_api_context(api_key_auth)
    return api_key_auth


async def check_access_token(
    access_token: APIContext = Depends(AccessTokenAuth())
) -> APIContext:
    """

    :param access_token:
    :return:
    """
    if not access_token:
        raise UnauthorizedException()
    set_api_context(access_token)
    return access_token


async def check_two_factor_token(
    two_factor_token: APIContext = Depends(TwoFactorTokenAuth())
) -> APIContext:
    """

    :param two_factor_token:
    :return:
    """
    if not two_factor_token:
        raise UnauthorizedException()
    set_api_context(two_factor_token)
    return two_factor_token
