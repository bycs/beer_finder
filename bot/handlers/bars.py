from django.db.models.query import QuerySet
from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes

from beers.models.bars import Bar
from bot.db import db
from bot.db import logging_commands


async def command_bars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None, "update.message must not be None"

    bars: QuerySet = Bar.objects.order_by("name").values("name", "website").distinct()
    bars_text = ""
    for bar in bars:
        bars_text += f"🍻 {bar['name']}\nСайт: {bar['website']}\n\n"
    text = "Сейчас мы знаем о следующих барах:\n\n" + bars_text
    await update.message.reply_text(text, disable_web_page_preview=True)
    logging_commands(db, update, "bars")


handler_bars = CommandHandler("bars", command_bars)
