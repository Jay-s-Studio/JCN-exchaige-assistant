"""
User API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.containers import Container
from app.handlers import UserHandler
from app.libs.contexts.api_context import APIContext, get_api_context
from app.libs.depends import (
    check_access_token,
    check_two_factor_token,
    DEFAULT_RATE_LIMITERS,
)
from app.route_classes import LogRoute
from app.serializers.v1.user import (
    UserLogin,
    LoginResponse,
    UserInfoResponse,
    UserRegister,
    UserBase,
    VerifyOTP,
    OTPInfo,
    TwoFactorVerify,
    TokenResponse,
    ChangePassword,
)

router = APIRouter(
    dependencies=DEFAULT_RATE_LIMITERS,
    route_class=LogRoute
)


@router.post(
    path="/register",
    response_model=UserBase
)
@inject
async def register(
    model: UserRegister,
    user_handler: UserHandler = Depends(Provide[Container.user_handler])
):
    """

    :param model:
    :param user_handler:
    :return:
    """
    return await user_handler.register(model=model)


@router.get(
    path="/info",
    response_model=UserInfoResponse,
    dependencies=[
        Depends(check_access_token)
    ]
)
@inject
async def get_user_info(
    api_context: APIContext = Depends(get_api_context),
    user_handler: UserHandler = Depends(Provide[Container.user_handler])
):
    """

    :param api_context:
    :param user_handler:
    :return:
    """
    return await user_handler.get_user_info(user_id=api_context.user_id)


@router.post(
    path="/login",
    response_model=LoginResponse
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
    path="/2fa_verify",
    response_model=TokenResponse,
    dependencies=[
        Depends(check_two_factor_token)
    ]
)
@inject
async def two_factor_auth_verify(
    model: TwoFactorVerify,
    api_context: APIContext = Depends(get_api_context),
    user_handler: UserHandler = Depends(Provide[Container.user_handler])
):
    """

    :param model:
    :param api_context:
    :param user_handler:
    :return:
    """
    return await user_handler.two_factor_auth_verify(
        user_id=api_context.user_id,
        model=model
    )


@router.post(
    path="/change_password",
    dependencies=[
        Depends(check_access_token)
    ]
)
@inject
async def change_password(
    model: ChangePassword,
    api_context: APIContext = Depends(get_api_context),
    user_handler: UserHandler = Depends(Provide[Container.user_handler])
):
    """

    :param model:
    :param api_context:
    :param user_handler:
    :return:
    """
    await user_handler.change_password(
        user_id=api_context.user_id,
        model=model
    )
    return {"message": "success"}


@router.post(
    path="/reset_2fa",
    dependencies=[
        Depends(check_access_token)
    ]
)
@inject
async def reset_2fa(
    model: TwoFactorVerify,
    api_context: APIContext = Depends(get_api_context),
    user_handler: UserHandler = Depends(Provide[Container.user_handler])
):
    """

    :param model:
    :param api_context:
    :param user_handler:
    :return:
    """
    await user_handler.reset_2fa(user_id=api_context.user_id, model=model)
    return {"message": "success"}


@router.get(
    path="/new_otp_info",
    response_model=OTPInfo,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(check_access_token)
    ]
)
@inject
async def generate_otp_info(
    api_context: APIContext = Depends(get_api_context),
    user_handler: UserHandler = Depends(Provide[Container.user_handler])
):
    """

    :param api_context:
    :param user_handler:
    :return:
    """
    return await user_handler.generate_new_otp_info(user_id=api_context.user_id)


@router.post(
    path="/verify_new_otp",
    dependencies=[
        Depends(check_access_token)
    ]
)
@inject
async def verify_new_otp(
    model: VerifyOTP,
    api_context: APIContext = Depends(get_api_context),
    user_handler: UserHandler = Depends(Provide[Container.user_handler])
):
    """

    :param model:
    :param user_handler:
    :param api_context:
    :return:
    """
    await user_handler.verify_otp(
        user_id=api_context.user_id,
        previous_otp=model.previous_otp,
        otp=model.otp
    )
    return {"message": "success"}
