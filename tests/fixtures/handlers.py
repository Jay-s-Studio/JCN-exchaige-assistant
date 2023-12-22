"""
Fixtures for handlers
"""
import pytest

from app.handlers.user import UserHandler
from app.containers import Container


@pytest.fixture
def user_handler() -> UserHandler:
    """
    user_handler
    :return:
    """
    return Container.user_handler()
