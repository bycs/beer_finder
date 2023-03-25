from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext.filters import Chat

from bot.utils.statistics import get_number_unique_users_text
from bot.utils.statistics import get_number_use_command_text
from config import TELEGRAM_ADMINS_ID


async def command_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None, "update.message must not be None"

    await update.message.reply_text(get_number_use_command_text())
    await update.message.reply_text(get_number_unique_users_text())


handler_statistics = CommandHandler(
    "statistics", command_statistics, filters=Chat(TELEGRAM_ADMINS_ID)
)
