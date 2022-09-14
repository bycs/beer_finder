from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup


class FilterForm(StatesGroup):
    bar = State()
    search_terms = State()
