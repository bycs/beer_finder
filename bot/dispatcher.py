import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.logics.base import BaseLogic
from bot.logics.filter_beers import FilterBeers
from bot.logics.on_startup import on_startup
from config import BOT_TOKEN


API_TOKEN = BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def run_bot() -> None:
    print("### The bot is being launched")
    BaseLogic(dp)
    FilterBeers(dp)
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
