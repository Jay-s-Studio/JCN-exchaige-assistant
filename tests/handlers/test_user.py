"""
Test user handler
"""
import pytest

from app.handlers.user import UserHandler
from app.serializers.v1.user import UserRegister, UserLogin


@pytest.mark.asyncio
async def test_create_user(user_handler: UserHandler):
    """
    Test create_user
    :param user_handler:
    :return:
    """
    model = UserRegister(
        username="test",
        password="test123"
    )
    await user_handler.create_user(model=model)


@pytest.mark.asyncio
async def test_login(user_handler: UserHandler):
    """
    Test login
    :param user_handler:
    :return:
    """
    user = await user_handler.login(
        model=UserLogin(
            username="test",
            password="test123"
        )
    )
    assert user is not None
    assert not hasattr(user, "hash_password")
    assert not hasattr(user, "password_salt")
