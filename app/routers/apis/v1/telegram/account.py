"""
Telegram Account API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.containers import Container
from app.handlers.telegram import TelegramAccountHandler
from app.libs.auth.bearer_jwt import BearerJWTAuth
from app.routing import LogRouting

router = APIRouter(dependencies=[Depends(BearerJWTAuth())], route_class=LogRouting)


@router.get(
    path="/vendors"
)
@inject
async def get_vendors(
    telegram_account_handler: TelegramAccountHandler = Depends(Provide[Container.telegram_account_handler])
):
    """

    :param telegram_account_handler:
    :return:
    """
    return await telegram_account_handler.get_vendors()
