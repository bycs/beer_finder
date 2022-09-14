from aiogram import Dispatcher
from aiogram import types


class BaseLogic:
    def __init__(self, dp: Dispatcher) -> None:
        self._register(dp)

    def _register(self, dp: Dispatcher) -> None:
        dp.register_message_handler(self.command_start, commands="start")
        dp.register_message_handler(self.command_help, commands="help")

    @staticmethod
    async def command_start(message: types.Message) -> None:
        text = "Привет!\nЯ твой лучший бот!\n\nPowered for Beer Finder."
        await message.reply(text)

    @staticmethod
    async def command_help(message: types.Message) -> None:
        text = "За помощью обращайся к @DD506"
        await message.reply(text)
