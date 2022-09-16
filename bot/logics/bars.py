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
        dp.register_message_handler(self.addresses_step2, state=AddressForm.bar)
        dp.register_message_handler(self.addresses_finish, state=AddressForm.metro)

    @staticmethod
    async def addresses_start(message: types.Message) -> None:
        await AddressForm.bar.set()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        bars = get_bars().values_list("name", flat=True)
        markup.add(*bars)
        markup.add("Любой бар")

        await message.reply("Выбери бар (кнопкой)", reply_markup=markup)

    @staticmethod
    async def addresses_step2(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            if message.text == "Любой бар":
                data["bar"] = None
            else:
                data["bar"] = message.text
            await AddressForm.next()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            bars_branch = get_bars_branches(data["bar"])
            data["bars_branch"] = bars_branch
            metro_list = list(bars_branch.values_list("metro", flat=True))
            metro_list.sort()
            markup.add(*metro_list)
            markup.add("Показать все")

            await message.reply("Выбери станцию метро (кнопкой)", reply_markup=markup)

    @staticmethod
    async def addresses_finish(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            if message.text == "Показать все":
                data["metro"] = None
                bars_branch = data["bars_branch"]
            else:
                data["metro"] = message.text
                bars_branch = data["bars_branch"].filter(metro=data["metro"])
            markup = types.ReplyKeyboardRemove()

            bars_branch_list = list(bars_branch)
            if len(bars_branch_list) == 0:
                response_text = "К сожалению, мы пока не можем найти такой адрес."
            else:
                text = ""
                for bar in bars_branch_list:
                    text += f"🍻 {bar.bar_branch_name}\n📍 {bar.address}\n{bar.bar.website}\n\n"
                response_text = "Сейчас мы знаем о следующих адресах:\n\n" + text

            await message.reply(response_text, reply_markup=markup)

        await state.finish()
