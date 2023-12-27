"""User Router"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Header
from starlette.requests import Request

from app.containers import Container
from app.handlers import UserHandler
from app.serializers.v1.user import UserLogin, LoginResponse, RefreshToken, TokenResponse

router = APIRouter()


@router.post(
    path="/login",
    response_model=LoginResponse,
)
@inject
async def login(
    model: UserLogin,
    user_handler: UserHandler = Depends(Provide[Container.user_handler])
):
    """

    :param model:
    :param user_handler:
    :return:
    """
    return await user_handler.login(model=model)


@router.post(
    path="/refresh_token",
    response_model=TokenResponse,
)
@inject
async def refresh_token(
    model: RefreshToken,
    authorization: str = Header(...),
    user_handler: UserHandler = Depends(Provide[Container.user_handler])
):
    """

    :param model:
    :param authorization:
    :param user_handler:
    :return:
    """
    token = authorization.split(" ")[1]
    return await user_handler.refresh_token(user_id=model.user_id.hex, token=token)
