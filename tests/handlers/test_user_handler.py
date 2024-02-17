"""
Test user handler
"""
from datetime import datetime, timedelta
from uuid import UUID

import pytest
from fastapi import HTTPException

from app.handlers import UserHandler
from app.serializers.v1.user import UserRegister, UserLogin


@pytest.mark.asyncio
async def test_create_user(user_handler: UserHandler):
    """
    Test create_user
    :param user_handler:
    :return:
    """
    model = UserRegister(
        email="admin@dummy.com",
        username="admin1",
        password="!QAZ2wsx3edc4rfv",
        confirm_password="!QAZ2wsx3edc4rfv",
    )
    await user_handler.register(model=model)


@pytest.mark.asyncio
async def test_create_user_with_week_password(user_handler: UserHandler):
    """
    Test create_user
    :param user_handler:
    :return:
    """
    model = UserRegister(
        email="account1@dummy.com",
        username="account1",
        password="abcdefg",
        confirm_password="abcdefg",
    )
    with pytest.raises(HTTPException) as exc:
        await user_handler.register(model=model)

    assert exc.type == HTTPException


@pytest.mark.asyncio
async def test_get_user_info(user_handler: UserHandler):
    """
    Test get_user_info
    :param user_handler:
    :return:
    """
    user_id = UUID("54737ccd-8fbf-4fea-a31b-e4e938a75237")
    user = await user_handler.get_user_info(user_id=user_id)
    assert user is not None
    assert user.username == "admin"


@pytest.mark.asyncio
async def test_login(user_handler: UserHandler):
    """
    Test login
    :param user_handler:
    :return:
    """
    user = await user_handler.login(
        model=UserLogin(
            username="admin",
            password="!QAZ2wsx3edc4rfv"
        )
    )
    assert user is not None
    assert user.access_token is not None
    assert user.token_type == "Bearer"


@pytest.mark.asyncio
async def test_generate_otp_secret(user_handler: UserHandler):
    """
    Test generate_otp_secret
    :param user_handler:
    :return:
    """
    user_id = UUID("54737ccd-8fbf-4fea-a31b-e4e938a75237")
    secret = await user_handler.generate_new_otp_info(user_id=user_id)
    assert secret is not None


@pytest.mark.asyncio
async def test_verify_otp(user_handler: UserHandler):
    """
    Test verify_otp
    :param user_handler:
    :return:
    """
    import pyotp
    user_id = UUID("54737ccd-8fbf-4fea-a31b-e4e938a75237")
    secret = await user_handler.generate_new_otp_info(user_id=user_id)
    totp = pyotp.TOTP(secret)
    previous_otp = totp.at(datetime.now() - timedelta(seconds=30))
    otp = totp.now()
    result = await user_handler.verify_otp(user_id=user_id, previous_otp=previous_otp, otp=otp)
