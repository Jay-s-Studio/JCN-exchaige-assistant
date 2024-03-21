"""
Telegram Messages API Router
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, BackgroundTasks
from starlette import status

from app.containers import Container
from app.handlers.telegram import TelegramMessageHandler
from app.libs.depends import check_all_authenticators, DEFAULT_RATE_LIMITERS
from app.route_classes import LogRoute
from app.serializers.v1.telegram import (
    TelegramBroadcast,
    PaymentAccount,
    ConfirmPay,
    OrderPaymentAccountStatus, GroupPaymentAccountStatus,
)

router = APIRouter(
    dependencies=[
        Depends(check_all_authenticators),
        *DEFAULT_RATE_LIMITERS
    ],
    route_class=LogRoute
)


@router.post(
    path="/broadcast",
    status_code=status.HTTP_202_ACCEPTED
)
@inject
async def broadcast(
    model: TelegramBroadcast,
    background_tasks: BackgroundTasks,
    telegram_message_handler: TelegramMessageHandler = Depends(Provide[Container.telegram_message_handler])
):
    """

    :param model:
    :param background_tasks:
    :param telegram_message_handler:
    :return:
    """
    background_tasks.add_task(telegram_message_handler.broadcast_message, model=model)
    return {"message": "accepted"}


@router.post(
    path="/payment_account",
    status_code=status.HTTP_200_OK
)
@inject
async def receive_payment_account(
    model: PaymentAccount,
    telegram_message_handler: TelegramMessageHandler = Depends(Provide[Container.telegram_message_handler])
):
    """

    :param model:
    :param telegram_message_handler:
    :return:
    """
    await telegram_message_handler.receive_payment_account(model=model)
    return {"message": "success"}


@router.put(
    path="/payment_account_status/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def update_payment_account_status(
    group_id: int,
    model: GroupPaymentAccountStatus,
    telegram_message_handler: TelegramMessageHandler = Depends(Provide[Container.telegram_message_handler])
):
    """

    :param group_id:
    :param model:
    :param telegram_message_handler:
    :return:
    """
    return await telegram_message_handler.update_payment_account_status(
        group_id=group_id,
        model=model
    )


@router.put(
    path="/order_payment_account_status/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def update_group_payment_account_status(
    group_id: int,
    model: OrderPaymentAccountStatus,
    telegram_message_handler: TelegramMessageHandler = Depends(Provide[Container.telegram_message_handler])
):
    """

    :param group_id:
    :param model:
    :param telegram_message_handler:
    :return:
    """
    return await telegram_message_handler.order_payment_account_status(
        group_id=group_id,
        model=model
    )


@router.post(
    path="/confirm_pay",
    status_code=status.HTTP_200_OK
)
@inject
async def confirm_pay(
    model: ConfirmPay,
    telegram_message_handler: TelegramMessageHandler = Depends(Provide[Container.telegram_message_handler])
):
    """

    :param model:
    :param telegram_message_handler:
    :return:
    """
    return await telegram_message_handler.confirm_pay(model=model)
