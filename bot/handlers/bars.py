from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes

from beers.logics.utils import get_bars
from bot.db import db
from bot.db import logging_commands


async def command_bars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None, "update.message must not be None"

    bars = list(get_bars())
    bars_text = ""
    for bar in bars:
        bars_text += f"🍻 {bar.name}\nСайт: {bar.website}\n\n"
    text = "Сейчас мы знаем о следующих барах:\n\n" + bars_text
    await update.message.reply_text(text)
    logging_commands(db, update, "bars")


handler_bars = CommandHandler("bars", command_bars)
