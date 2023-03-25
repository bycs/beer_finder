from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler
from telegram.ext import MessageHandler
from telegram.ext import filters

from beers.logics.utils import filter_beers
from beers.logics.utils import get_top_keys
from beers.logics.utils import get_top_values
from beers.models.beers import Beer
from bot.db import db
from bot.db import logging_commands
from bot.db import logging_search_query
from bot.handlers.bar_branch_geo import choosing_bar
from bot.utils.utils import list_separator


async def beer_filter_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    assert update.message is not None, "update.message must not be None"
    assert context.user_data is not None, "context.user_data must not be None"

    if update.message.text == "Любой бар":
        bar = None
    else:
        bar = update.message.text

    context.user_data["beer_filter"] = {"bar": bar}
    keys = get_top_keys(6, bar)
    keyboard_keys = list_separator(list(keys), 3)
    keyboard = [*keyboard_keys, ["Показать все"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, selective=True)
    text = "Выбери фильтр (кнопкой)"
    await update.message.reply_text(text, reply_markup=markup)
    return "step_3"


async def beer_filter_step_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    assert update.message is not None, "update.message must not be None"
    assert update.message.text is not None, "update.message.text must not be None"
    assert context.user_data is not None, "context.user_data must not be None"

    if update.message.text == "Показать все":
        search_terms = None
        context.user_data["beer_filter"]["search_terms"] = search_terms
        keyboard = [["Показать результаты"]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, selective=True)
        text = "Попробуй в следующий раз поставить фильтры"
        await update.message.reply_text(text, reply_markup=markup)
        logging_commands(db, update, "beer_filter__step_3")
        return "finish"
    else:
        search_terms = update.message.text

    context.user_data["beer_filter"]["search_terms"] = search_terms
    bar = context.user_data["beer_filter"]["bar"]
    values = get_top_values(search_terms, 6, bar)
    keyboard_values = list_separator(list(values), 3)
    keyboard = [*keyboard_values, ["Показать все"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, selective=True)
    text = "Выбери фильтр (кнопкой)"
    await update.message.reply_text(text, reply_markup=markup)
    return "finish"


async def beer_filter_finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message is not None, "update.message must not be None"
    assert context.user_data is not None, "context.user_data must not be None"

    markup = ReplyKeyboardRemove()
    if update.message.text == "Показать все" or update.message.text == "Показать результаты":
        request = None
    else:
        request = update.message.text

    context.user_data["beer_filter"]["request"] = request
    bar = context.user_data["beer_filter"]["bar"]
    search_terms: str = context.user_data["beer_filter"]["search_terms"]

    bar_text = get_bar_text(bar)
    search_text = get_search_text_text(search_terms, request)
    filter_dict = {search_terms: request}
    beers = filter_beers(bar, 5, filter_dict)
    count_beers = len(beers)
    answer_text = f"\n\nЯ сформировал специально для тебя {count_beers} сортов пива:"
    text = bar_text + search_text + answer_text
    await update.message.reply_text(text, reply_markup=markup)
    for beer in beers:
        name_text = f"🍻 {beer.name}\n"
        bar_text = f"Бар: #{beer.bar.name.replace(' ', '')}\n"
        description_text = get_description_text(beer)
        price_text = get_price_text(beer)
        specifications_text = get_specifications_text(beer)
        text = name_text + price_text + bar_text + description_text + specifications_text
        await update.message.reply_text(text)
    search_query = context.user_data["beer_filter"]
    logging_search_query(db, update, search_query, "beer_filter")
    logging_commands(db, update, "beer_filter")
    return ConversationHandler.END


handler_beer_filter = ConversationHandler(
    entry_points=[CommandHandler("beer_filter", choosing_bar)],
    states={
        "step_2": [MessageHandler(filters.TEXT, beer_filter_step_2)],
        "step_3": [MessageHandler(filters.TEXT, beer_filter_step_3)],
        "finish": [MessageHandler(filters.TEXT, beer_filter_finish)],
    },
    fallbacks=[],
)


def get_bar_text(bar: str | None) -> str:
    if bar is None:
        bar = "Любой"
    return f"Бар: {bar}\n"


def get_price_text(beer: Beer) -> str:
    if beer.price:
        return f"Цена ~{beer.price_rub} ₽/л\n"
    return ""


def get_search_text_text(
    search_terms: str | None,
    request: str | None,
) -> str:
    if search_terms is None or request is None:
        return "Критерии поиска отсутствуют"
    return f"Критерии поиска:\n{search_terms} = {request}"


def get_specifications_text(beer: Beer) -> str:
    if beer.specifications:
        specifications_text = ""
        for key, value in beer.specifications.items():
            specifications_text += f"\n{key}: {value}"
        return specifications_text
    return ""


def get_description_text(beer: Beer) -> str:
    if beer.description:
        return f"\nОписание: {beer.description}\n"
    return ""
