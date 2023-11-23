"""
Telegram bot application
"""
import telegram
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters, ChatMemberHandler

from app.config import settings
from app.context import CustomContext
from app.handlers.bot_handler import start, track_chats, echo, show_chats, greet_chat_members, get_my_information

__all__ = ["application", "bot"]

_context_types = ContextTypes(context=CustomContext)

bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
application = (
    Application.builder()
    .token(settings.TELEGRAM_BOT_TOKEN)
    .context_types(_context_types)
    .build()
)

# register handlers
application.add_handler(CommandHandler(command="start", callback=start))
# Keep track of which chats the bot is in
application.add_handler(ChatMemberHandler(callback=track_chats))
application.add_handler(CommandHandler(command="show_chats", callback=show_chats))
application.add_handler(CommandHandler(command="my_account", callback=get_my_information))

# Handle members joining/leaving chats.
application.add_handler(MessageHandler(filters=filters.StatusUpdate.NEW_CHAT_MEMBERS, callback=greet_chat_members))

application.add_handler(MessageHandler(filters=filters.TEXT & filters.UpdateType.MESSAGES & ~filters.COMMAND, callback=echo))
