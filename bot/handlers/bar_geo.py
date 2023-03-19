from collections import Counter
from operator import itemgetter

from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler
from telegram.ext import MessageHandler
from telegram.ext import filters

from beers.logics.geo import Point
from beers.logics.geo import YandexMapGeo
from beers.logics.geo import get_distance
from beers.logics.utils import get_bars
from beers.logics.utils import get_bars_branches
from bot.db import db
from bot.db import logging_commands


async def choosing_bar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    bars = get_bars().values_list("name", flat=True)
    keyboard = [[*bars], ["Любой бар"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, selective=True)
    text = "Выбери бар (кнопкой)"
    await update.message.reply_text(text, reply_markup=markup)  # type: ignore[union-attr]
    logging_commands(db, update, "bar_branch_geo__start")
    return "step_2"


async def get_address_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    if update.message.text == "Любой бар":  # type: ignore[union-attr]
        context.user_data["bar_branch_geo"] = {"bar": None}  # type: ignore[index]
    else:
        context.user_data["bar_branch_geo"] = {"bar": update.message.text}  # type: ignore

    keyboard = [[KeyboardButton("📍 Отправить геопозицию", request_location=True)]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, selective=True)
    text = "Отправьте геопозицию или введите адрес"
    await update.message.reply_text(text, reply_markup=markup)  # type: ignore[union-attr]
    logging_commands(db, update, "bar_branch_geo__step_2")
    return "finish"


async def bar_branch_geo_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = ReplyKeyboardRemove()
    if update.message.location:  # type: ignore[union-attr]
        context.user_data["bar_branch_geo"]["search_type"] = "location"  # type: ignore
        longitude = update.message.location.longitude  # type: ignore[union-attr]
        latitude = update.message.location.latitude  # type: ignore[union-attr]
        location_user = Point(latitude, longitude)

    else:
        context.user_data["bar_branch_geo"]["search_type"] = "address"  # type: ignore[index]
        geo = YandexMapGeo()
        point = geo.geocode(update.message.text)  # type: ignore
        if point:
            location_user = point
        else:
            text = "Не удалось определить кооринаты 🤷🏻‍"
            await update.message.reply_text(text, reply_markup=markup)  # type: ignore[union-attr]
            logging_commands(db, update, "bar_branch_geo__finish")
            return ConversationHandler.END

    bars_branch = get_bars_branches(context.user_data["bar_branch_geo"]["bar"])  # type: ignore
    distances = {}
    for bar in bars_branch:
        point_bar = bar.point.split(",")
        location_bar = Point(float(point_bar[0]), float(point_bar[1]))
        distance = get_distance(location_user, location_bar)
        distances[bar] = round(distance / 1000, 1)

    distances_dict = dict(Counter(distances))
    distances_tuple = sorted(distances_dict.items(), key=itemgetter(1))
    distances_sorted = dict(distances_tuple[:3])

    if len(distances_sorted) == 0:
        response_text = "К сожалению, мы не смогли ничего найти, попробуйте еще раз."
    else:
        text = ""
        for bar in distances_sorted:
            ya = "https://yandex.ru/maps/"
            maps_link = f"{ya}?ll={bar.point}&z=16&text={bar.bar.name.replace(' ', '%20')}"
            # address = md.hlink(bar.address, maps_link)
            address = f"<a href='{maps_link}'>{bar.address}</a>"
            address_text = f"📍 {address}\n\n"
            name_text = f"🍻 {bar.barbranch_name} ~{distances_sorted[bar]} км\n"
            website_text = f"{bar.bar.website}\n\n\n"
            text += name_text + address_text + website_text
        response_text = "Самые близкие бары:\n\n" + text

    await update.message.reply_text(  # type: ignore[union-attr]
        response_text,
        reply_markup=markup,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    logging_commands(db, update, "bar_branch_geo__finish")
    return ConversationHandler.END


handler_barbranch_geo = ConversationHandler(
    entry_points=[CommandHandler("bar_branch_geo", choosing_bar)],
    states={
        "step_2": [MessageHandler(filters.TEXT, get_address_user)],
        "finish": [MessageHandler(filters.TEXT | filters.LOCATION, bar_branch_geo_finish)],
    },
    fallbacks=[],
)
