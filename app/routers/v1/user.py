"""User Router"""
from fastapi import APIRouter
from starlette.requests import Request
from app.serializers.v1.user import UserLogin

router = APIRouter()


@router.post(
    path="/login"
)
async def login(
    model: UserLogin
):
    """

    :param model:
    :return:
    """
