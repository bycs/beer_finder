from aiogram import Dispatcher
from aiogram import types


class BaseLogic:
    def __init__(self, dp: Dispatcher) -> None:
        self._register(dp)

    def _register(self, dp: Dispatcher) -> None:
        raise NotImplementedError


class Basic(BaseLogic):
    def _register(self, dp: Dispatcher) -> None:
        dp.register_message_handler(self.command_start, commands="start")
        dp.register_message_handler(self.command_help, commands="help")

    @staticmethod
    async def command_start(message: types.Message) -> None:
        text = "Привет!\nЯ постараюсь помочь тебе с выбором пенного!\n\nPowered by Python 🐍"

        disclaimer = """
Здесь содержится информацию, которая не рекомендована лицам, не достигшим совершеннолетия.\n
Продолжая пользоваться ботом, Вы подтверждаете, что вам больше 18 лет.\n
🔞 Чрезмерное употребление алкоголя вредит Вашему здоровью."""
        await message.reply(text)
        await message.answer(disclaimer)

    @staticmethod
    async def command_help(message: types.Message) -> None:
        text = "За помощью обращайся к @DD506"
        await message.reply(text)
