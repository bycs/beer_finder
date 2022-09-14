from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.forms import FilterForm


class FilterBeers:
    def __init__(self, dp: Dispatcher) -> None:
        self._register(dp)

    def _register(self, dp: Dispatcher) -> None:
        dp.register_message_handler(self.filter_start, commands="filter")
        dp.register_message_handler(self.filter_step2, state=FilterForm.bar)
        dp.register_message_handler(self.filter_finish, state=FilterForm.search_terms)

    @staticmethod
    async def filter_start(message: types.Message) -> None:
        await FilterForm.bar.set()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Бар 1", "Бар 2", "Бар 3")
        markup.add("Не хочу выбирать бар")

        await message.reply("Выбери бар (кнопкой)", reply_markup=markup)

    @staticmethod
    async def filter_step2(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            data["bar"] = message.text

            await FilterForm.next()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add("Сорт", "Изготовитель")
            markup.add("Пропуск")

            await message.reply("Выбери фильтр (кнопкой)", reply_markup=markup)

    @staticmethod
    async def filter_finish(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            data["search_terms"] = message.text
            markup = types.ReplyKeyboardRemove()
            text = f"Ура!\n\nТы выбрал Бар: {data['bar']}\nУсловия поиска: {data['search_terms']}"
            await message.reply(text, reply_markup=markup)

        await state.finish()
