from random import shuffle

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
from bot.db import db
from bot.db import logging_commands
from bot.handlers.bar_branch_geo import choosing_bar


async def beer_filter_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    assert update.message is not None, "update.message must not be None"
    assert context.user_data is not None, "context.user_data must not be None"

    if update.message.text == "Любой бар":
        bar = None
    else:
        bar = update.message.text

    context.user_data["beer_filter"] = {"bar": bar}
    keys = get_top_keys(bar)
    keyboard_keys = [keys[i : i + 3] for i in range(0, len(keys), 3)]
    keyboard = [*keyboard_keys, ["Показать все"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, selective=True)

    text = "Выбери фильтр (кнопкой)"
    await update.message.reply_text(text, reply_markup=markup)
    logging_commands(db, update, "beer_filter__step_2")
    return "step_3"


async def beer_filter_step_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    assert update.message is not None, "update.message must not be None"
    assert context.user_data is not None, "context.user_data must not be None"

    if update.message.text == "Показать все":
        search_terms = None
    else:
        search_terms = update.message.text

    context.user_data["beer_filter"]["search_terms"] = search_terms
    bar = context.user_data["beer_filter"]["bar"]
    values = get_top_values(bar, search_terms)
    keyboard_values = [values[i : i + 3] for i in range(0, len(values), 3)]
    keyboard = [*keyboard_values, ["Показать все"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, selective=True)
    text = "Выбери фильтр (кнопкой)"
    await update.message.reply_text(text, reply_markup=markup)
    logging_commands(db, update, "beer_filter__step_3")
    return "finish"


async def beer_filter_finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    assert update.message is not None, "update.message must not be None"
    assert context.user_data is not None, "context.user_data must not be None"

    markup = ReplyKeyboardRemove()
    if update.message.text == "Показать все":
        request = None
    else:
        request = update.message.text

    context.user_data["beer_filter"]["request"] = request
    bar = context.user_data["beer_filter"]["bar"]
    search_terms = context.user_data["beer_filter"]["search_terms"]

    bar_text = f"Бар: {bar}\n"
    search_text = f"Критерии поиска: {search_terms}: {request}"
    answer_text = "\n\nЯ сформировал для тебя 5 случайных пива, которые тебе понравятся:"
    text = bar_text + search_text + answer_text
    await update.message.reply_text(text, reply_markup=markup)
    filter_dict = {search_terms: request}
    beers = list(filter_beers(bar, filter_dict))
    shuffle(beers)
    if len(beers) > 5:
        beers = beers[:5]
    for beer in beers:
        name_text = f"🍻 {beer.name}\n"
        bar_text = f"Бар: #{beer.bar.name.replace(' ', '')}\n"
        description_text = f"\nОписание: {beer.description}\n"
        if beer.price:
            price_text = f"Цена ~{beer.price_rub} ₽/л\n"
        if beer.specifications:
            specifications_text = ""
            for key, value in beer.specifications.items():
                specifications_text += f"\n{key}: {value}"
        text = name_text + price_text + bar_text + description_text + specifications_text
        await update.message.reply_text(text)
    logging_commands(db, update, "beer_filter__finish")
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
