from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup


class AddressForm(StatesGroup):
    bar = State()
    metro = State()


class FilterForm(StatesGroup):
    bar = State()
    search_terms = State()
    request = State()
