from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes

from bot.db import db
from bot.db import logging_commands


async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None, "update.message must not be None"

    text = "Привет!\nЯ постараюсь помочь тебе с выбором пенного!\n\nPowered by Python 🐍"

    disclaimer = """
Здесь содержится информацию, которая не рекомендована лицам, не достигшим совершеннолетия.\n
Продолжая пользоваться ботом, Вы подтверждаете, что вам больше 18 лет.\n
🔞 Чрезмерное употребление алкоголя вредит Вашему здоровью."""

    await update.message.reply_text(text)
    await update.message.reply_text(disclaimer)
    logging_commands(db, update, "start")


handler_start = CommandHandler("start", command_start)


async def command_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None, "update.message must not be None"
    text = """Список команд:
/start - Запустить / обновить бота
/bars - Список баров
/bar_branch_geo - Поиск ближайшего бара
/bar_branch_list - Поиск бара по метро
/beer_filter - Подбор пива
/help - Помощь"""
    text += "\n\nПо другим вопросам обращайся к @DD506"
    await update.message.reply_text(text)
    logging_commands(db, update, "help")


handler_help = CommandHandler("help", command_help)
