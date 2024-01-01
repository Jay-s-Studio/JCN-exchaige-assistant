"""
Test user handler
"""
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
        username="account1",
        password="!QAZ2wsx3edc4rfv",
    )
    await user_handler.create_user(model=model)


@pytest.mark.asyncio
async def test_create_user_with_week_password(user_handler: UserHandler):
    """
    Test create_user
    :param user_handler:
    :return:
    """
    model = UserRegister(
        username="account1",
        password="abcdefg",
    )
    with pytest.raises(HTTPException) as exc:
        await user_handler.create_user(model=model)

    assert exc.type == HTTPException


@pytest.mark.asyncio
async def test_login(user_handler: UserHandler):
    """
    Test login
    :param user_handler:
    :return:
    """
    user = await user_handler.login(
        model=UserLogin(
            username="account1",
            password="!QAZ2wsx3edc4rfv"
        )
    )
    assert user is not None
    assert user.access_token is not None
    assert user.token_type == "Bearer"
