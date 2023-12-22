"""
Test user provider
"""
import pytest

from app.providers import UserProvider


@pytest.mark.asyncio
async def test_get_user_by_username(user_provider: UserProvider):
    """
    Test get user by username
    """
    user = await user_provider.get_user_by_username(username='test')
    assert user is not None
