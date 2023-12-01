#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handlers functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the app is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
app.
"""
import asyncio
import html
from typing import Optional, Tuple
from urllib.parse import urljoin

from dependency_injector.wiring import inject, Provide
from telegram import Update, Chat, ChatMemberUpdated, ChatMember

from app.config import settings
from app.containers import Container
from app.context import CustomContext
from app.libs.logger import logger
from app.models.account.telegram import TelegramAccount
from app.providers import TelegramAccountProvider


async def start(update: Update, context: CustomContext) -> None:
    """
    Send a message when the command /start is issued.
    :param update:
    :param context:
    :return:
    """
    user = update.effective_user
    payload_url = html.escape(urljoin(base=settings.BASE_URL, url=f"/submitpayload?user_id=<your user id>&payload=<payload>"))
    healthcheck_url = html.escape(urljoin(base=settings.BASE_URL, url=f"/healthcheck"))
    text = (
        f"Hi {user.mention_html()}!\n\n"
        f"To check if the app is still running, call <code>{healthcheck_url}</code>.\n\n"
        f"To post a custom update, call <code>{payload_url}</code>.\n\n"
        f"Your user id is <code>{user.id}</code>.\n\n"
    )
    await update.message.reply_html(text=text)


def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
    """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
    the status didn't change.
    """
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))
    logger.info(f"status_change: {status_change}")
    logger.info(f"old_is_member: {old_is_member}")
    logger.info(f"new_is_member: {new_is_member}")

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member


@inject
async def track_chats(
    update: Update,
    context: CustomContext,
    telegram_account_provider: TelegramAccountProvider = Provide[Container.telegram_account_provider]
) -> None:
    """
    Tracks the chats the bot is in.
    :param update:
    :param context:
    :param telegram_account_provider:
    :return:
    """
    logger.info(str.rjust("", 100, "-"))
    logger.info("track_chats")
    result = extract_status_change(update.my_chat_member)
    if result is None:
        return
    was_member, is_member = result

    # Let's check who is responsible for the change
    cause_name = update.effective_user.full_name

    # Handle chat types differently:
    chat = update.effective_chat
    logger.info(f"was_member: {was_member}, is_member: {is_member}")
    logger.info(f"chat: {chat.to_dict()}")
    if chat.type not in [Chat.GROUP, Chat.SUPERGROUP]:
        try:
            await chat.send_message(
                f"Sorry, This bot only work in groups. I'll leave now. Bye!"
            )
            await asyncio.sleep(2)
            await chat.leave()
        except Exception as exc:
            logger.exception(exc)

    data = chat.to_dict()
    data["in_group"] = is_member
    await telegram_account_provider.update_chat_group(chat_id=str(chat.id), data=data)


async def greet_chat_members(
    update: Update,
    context: CustomContext
) -> None:
    """
    Greets new users in chats and announces when someone leaves
    :param update:
    :param context:
    :return:
    """
    logger.info(str.rjust("", 100, "-"))
    logger.info("greet_chat_members")
    for new_member in update.message.new_chat_members:
        logger.info(new_member.to_dict())
    # result = extract_status_change(update.chat_member)
    # if result is None:
    #     return
    #
    # was_member, is_member = result
    # logger.info(f"was_member: {was_member}, is_member: {is_member}")
    # logger.info(f"from_user: {update.chat_member.from_user.to_dict()}")
    # logger.info(f"new_chat_member: {update.chat_member.new_chat_member.to_dict()}")
    #
    # cause_name = update.chat_member.from_user.mention_html()
    # member_name = update.chat_member.new_chat_member.user.mention_html()
    #
    # if not was_member and is_member:
    #     await update.effective_chat.send_message(
    #         f"{member_name} was added by {cause_name}. Welcome!",
    #         parse_mode=ParseMode.HTML,
    #     )
    # elif was_member and not is_member:
    #     await update.effective_chat.send_message(
    #         f"{member_name} is no longer with us. Thanks a lot, {cause_name} ...",
    #         parse_mode=ParseMode.HTML,
    #     )


@inject
async def get_my_information(
    update: Update,
    context: CustomContext,
    telegram_account_provider: TelegramAccountProvider = Provide[Container.telegram_account_provider]
) -> None:
    """
    Get my information
    :param update:
    :param context:
    :param telegram_account_provider:
    :return:
    """
    user = await telegram_account_provider.get_account(user_id=str(update.effective_user.id))
    if not user:
        await telegram_account_provider.set_account(user_id=str(update.effective_user.id), data=update.effective_user.to_dict())
        user = TelegramAccount(**update.effective_user.to_dict())
    text = (
        f"Your user id is <code>{user.id}</code>.\n\n"
        f"Your name is <code>{user.last_name}</code>.\n\n"
        f"Your username is <code>{user.username}</code>.\n\n"
    )
    await update.message.reply_html(text=text)


@inject
async def echo(
    update: Update,
    context: CustomContext,
    telegram_account_provider: TelegramAccountProvider = Provide[Container.telegram_account_provider]
) -> None:
    """
    Echo the user message.
    :param update:
    :param context:
    :param telegram_account_provider:
    :return:
    """
    user = update.effective_user.to_dict()
    await telegram_account_provider.set_account(user_id=str(update.effective_user.id), data=user)
    await update.effective_message.reply_text(update.message.text)
