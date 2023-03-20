import logging

from telegram import BotCommand
from telegram import Update
from telegram.ext import Application
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler

from bot.db import db
from bot.db import logging_commands
from bot.handlers.bar_branch_geo import handler_bar_branch_geo
from bot.handlers.bar_branch_list import handler_bar_branch_list
from bot.handlers.bars import handler_bars
from config import BOT_TOKEN


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log",
)


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

    text = "За помощью обращайся к @DD506"
    await update.message.reply_text(text)
    logging_commands(db, update, "help")


handler_help = CommandHandler("help", command_help)


async def post_init(application: Application) -> None:
    commands: list[BotCommand] = [
        BotCommand("start", "Запустить / обновить бота"),
        BotCommand("bars", "Список баров"),
        BotCommand("bar_branch_geo", "Поиск ближайшего бара"),
        BotCommand("bar_branch_list", "Поиск бара по метро"),
        BotCommand("help", "Помощь"),
    ]
    await application.bot.set_my_commands(commands)


handlers: list[CommandHandler | ConversationHandler] = [
    handler_start,
    handler_help,
    handler_bars,
    handler_bar_branch_geo,
    handler_bar_branch_list,
]


def run_bot() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()
    for handler in handlers:
        application.add_handler(handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
