"""
User API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.containers import Container
from app.handlers import UserHandler
from app.libs.contexts.api_context import APIContext, get_api_context
from app.libs.depends import check_all_authenticators, DEFAULT_RATE_LIMITERS
from app.route_classes import LogRoute
from app.serializers.v1.user import UserLogin, LoginResponse, TokenResponse, UserInfoResponse

router = APIRouter(
    dependencies=DEFAULT_RATE_LIMITERS,
    route_class=LogRoute
)


@router.get(
    path="/info",
    response_model=UserInfoResponse,
    dependencies=[
        Depends(check_all_authenticators)
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
