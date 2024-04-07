"""
Fixtures for controllers
"""
import pytest

from app.controllers import MessagesController
from app.containers import Container


@pytest.fixture
def messages_controller() -> MessagesController:
    """
    messages_controller
    :return:
    """
    return Container.messages_controller()
