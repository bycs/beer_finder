from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext

from beers.logics.utils import get_bars
from beers.logics.utils import get_bars_branches
from bot.forms import AddressForm
from bot.logics.base import BaseLogic


class BarHandler(BaseLogic):
    def _register(self, dp: Dispatcher) -> None:
        dp.register_message_handler(self.command_bars, commands="bars")

    @staticmethod
    async def command_bars(message: types.Message) -> None:
        bars = list(get_bars())
        bars_text = ""
        for bar in bars:
            bars_text += f"🍻 {bar.name}\nСайт: {bar.website}\n\n"
        text = "Сейчас мы знаем о следующих барах:\n\n" + bars_text
        await message.reply(text)


class BarBranchHandler(BaseLogic):
    def _register(self, dp: Dispatcher) -> None:
        dp.register_message_handler(self.addresses_start, commands="addresses")
        dp.register_message_handler(self.addresses_finish, state=AddressForm.bar)

    @staticmethod
    async def addresses_start(message: types.Message) -> None:
        await AddressForm.bar.set()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        bars = get_bars().values_list("name", flat=True)
        markup.add(*bars)
        markup.add("Любой бар")

        await message.reply("Выбери бар (кнопкой)", reply_markup=markup)

    @staticmethod
    async def addresses_finish(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            if message.text == "Любой бар":
                data["bar"] = None
            else:
                data["bar"] = message.text
            markup = types.ReplyKeyboardRemove()
            bars_branch = list(get_bars_branches(data["bar"]))
            if len(bars_branch) == 0:
                response_text = "К сожалению, мы пока не знаем адресов этого бара."
            else:
                text = ""
                for bar in bars_branch:
                    text += f"🍻 {bar.bar_branch_name}\n📍 {bar.address}\n{bar.bar.website}\n\n"
                response_text = "Сейчас мы знаем о следующих адресах:\n\n" + text

            await message.reply(response_text, reply_markup=markup)

        await state.finish()
