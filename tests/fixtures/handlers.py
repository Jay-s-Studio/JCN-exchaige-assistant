"""
Fixtures for handlers
"""
import pytest

from app.handlers.auth import AuthHandler
from app.handlers.user import UserHandler
from app.containers import Container


@pytest.fixture
def auth_handler() -> AuthHandler:
    """
    auth_handler
    :return:
    """
    return Container.auth_handler()


@pytest.fixture
def user_handler() -> UserHandler:
    """
    user_handler
    :return:
    """
    return Container.user_handler()
