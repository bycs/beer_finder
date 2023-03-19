import logging

from telegram import BotCommand
from telegram import Update
from telegram.ext import Application
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes

from bot.db import db
from bot.db import logging_commands
from config import BOT_TOKEN


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log",
)


async def post_init(application: Application) -> None:
    commands = [
        BotCommand("start", "Запустить / обновить бота"),
        BotCommand("help", "Помощь"),
    ]
    await application.bot.set_my_commands(commands)


async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "Привет!\nЯ постараюсь помочь тебе с выбором пенного!\n\nPowered by Python 🐍"

    disclaimer = """
Здесь содержится информацию, которая не рекомендована лицам, не достигшим совершеннолетия.\n
Продолжая пользоваться ботом, Вы подтверждаете, что вам больше 18 лет.\n
🔞 Чрезмерное употребление алкоголя вредит Вашему здоровью."""

    await update.message.reply_text(text)  # type: ignore
    await update.message.reply_text(disclaimer)  # type: ignore
    logging_commands(db, update.effective_user.id, update.message.chat.id, "start")  # type: ignore


handler_start = CommandHandler("start", command_start)


async def command_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = "За помощью обращайся к @DD506"
    await update.message.reply_text(text)  # type: ignore[union-attr]
    logging_commands(db, update.effective_user.id, update.message.chat.id, "help")  # type: ignore


handler_help = CommandHandler("help", command_help)


handlers: list[CommandHandler] = [
    handler_start,
    handler_help,
]


def run_bot() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()
    for handler in handlers:
        application.add_handler(handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
