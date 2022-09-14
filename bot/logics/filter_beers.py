from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext

from beers.logics.utils import filter_beers
from beers.logics.utils import get_bars
from beers.logics.utils import get_top_keys
from beers.logics.utils import get_top_values
from bot.forms import FilterForm


class FilterBeers:
    def __init__(self, dp: Dispatcher) -> None:
        self._register(dp)

    def _register(self, dp: Dispatcher) -> None:
        dp.register_message_handler(self.filter_start, commands="filter")
        dp.register_message_handler(self.filter_step2, state=FilterForm.bar)
        dp.register_message_handler(self.filter_step3, state=FilterForm.search_terms)
        dp.register_message_handler(self.filter_finish, state=FilterForm.request)

    @staticmethod
    async def filter_start(message: types.Message) -> None:
        await FilterForm.bar.set()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        bars = get_bars()
        markup.add(*bars)
        markup.add("Любой бар")

        await message.reply("Выбери бар (кнопкой)", reply_markup=markup)

    @staticmethod
    async def filter_step2(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            if message.text == "Любой бар":
                data["bar"] = None
            else:
                data["bar"] = message.text

            await FilterForm.next()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            keys = get_top_keys(data["bar"])
            markup.add(*keys)
            markup.add("Показать все")

            await message.reply("Выбери фильтр (кнопкой)", reply_markup=markup)

    @staticmethod
    async def filter_step3(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            if message.text == "Показать все":
                data["search_terms"] = None
            else:
                data["search_terms"] = message.text

            await FilterForm.next()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            values = get_top_values(data["bar"], data["search_terms"])
            markup.add(*values)
            markup.add("Показать все")

            await message.reply("Выбери фильтр (кнопкой)", reply_markup=markup)

    @staticmethod
    async def filter_finish(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            data["request"] = message.text
            markup = types.ReplyKeyboardRemove()
            text = f"Бар: {data['bar']}\nКритерии поиска: {data['search_terms']}: {data['request']}"
            await message.reply(text, reply_markup=markup)
            bar = data["bar"]
            filter_dict = {data["search_terms"]: data["request"]}
            beers = filter_beers(bar, filter_dict)
            for beer in beers:
                if beer.price:
                    price = f"{beer.price / 100} руб/л"
                text = f"{beer.name} - {price}\n{beer.description}"
                await message.answer(text)

        await state.finish()
