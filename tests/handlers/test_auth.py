"""
Test auth handlers
"""
from uuid import UUID

import pytest

from app.handlers import AuthHandler
from app.schemas.user import User

dummy_user = User(
    id=UUID("00000000-0000-0000-0000-000000000000"),
    username="test",
    display_name="test",
    email="",
    hash_password="test",
    password_salt="test",
    is_active=True
)


@pytest.mark.asyncio
async def test_generate_token(auth_handler: AuthHandler):
    """
    test_generate_token
    :param auth_handler:
    :return:
    """
    token = auth_handler.generate_token(user=dummy_user)
    assert isinstance(token, str)


@pytest.mark.asyncio
async def test_verify_token(auth_handler: AuthHandler):
    """
    test_verify_token
    :param auth_handler:
    :return:
    """
    token = auth_handler.generate_token(user=dummy_user)
    uid = auth_handler.verify_token(token=token)
    assert uid == "00000000-0000-0000-0000-000000000000"


@pytest.mark.asyncio
async def test_expired_token(auth_handler: AuthHandler):
    """
    test_expired_token
    :param auth_handler:
    :return:
    """
    token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJqY25fZXhjaGFpZ2VfYXNzaXN0YW50Iiwic3ViIjoidGVzdCIsInVpZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMCIsImlhdCI6MTcwMzMzOTQyNywiZXhwIjoxNzAzMzQzMDI3fQ.KY3hsttvKydpzp8FGDMGRq_3y-C9fTPiIB3kH74SnVpjbHi21Cf57U78GmQy0kuar-XkUkIsU-9oxdX8GUPgHA"
    auth_handler.verify_token(token=token)


@pytest.mark.asyncio
async def test_verify_otp(auth_handler: AuthHandler):
    """
    test_verify_otp
    :param auth_handler:
    :return:
    """
    secret = "SRBPLAIK2EQP4S6GGSSRRR7IBH6SOQJY"
    otp = "464606"
    result = auth_handler.verify_otp(secret=secret, otp=otp)
    assert result is True
