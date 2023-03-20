from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler
from telegram.ext import MessageHandler
from telegram.ext import filters

from beers.logics.utils import get_bars_branches
from bot.db import db
from bot.db import logging_commands
from bot.handlers.bar_branch_geo import choosing_bar


async def get_metro_bar_branch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    assert update.message is not None, "update.message must not be None"
    assert context.user_data is not None, "context.user_data must not be None"

    if update.message.text == "Любой бар":
        context.user_data["bar_branch_list"] = {"bar": None}
    else:
        context.user_data["bar_branch_list"] = {"bar": update.message.text}
    bar = context.user_data["bar_branch_list"]["bar"]
    bars_branch = get_bars_branches(bar)
    context.user_data["bar_branch_list"]["bars_branch"] = bars_branch
    metro_list = list(bars_branch.values_list("metro", flat=True))
    metro_list = list(set(metro_list))
    metro_list.sort()
    keyboard_metro = [metro_list[i : i + 3] for i in range(0, len(metro_list), 3)]
    keyboard = [*keyboard_metro, ["Показать все"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, selective=True)
    text = "Выбери станцию метро (кнопкой)"
    await update.message.reply_text(text, reply_markup=markup)
    logging_commands(db, update, "bar_branch_list__step_2")
    return "finish"


async def bar_branch_list_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.message is not None, "update.message must not be None"
    assert context.user_data is not None, "context.user_data must not be None"

    markup = ReplyKeyboardRemove()
    if update.message.text == "Показать все":
        context.user_data["bar_branch_list"]["metro"] = None
        bars_branch = context.user_data["bar_branch_list"]["bars_branch"]
    else:
        context.user_data["bar_branch_list"]["metro"] = update.message.text
        bars_branch = context.user_data["bar_branch_list"]["bars_branch"]
        bars_branch = bars_branch.filter(metro=update.message.text)

    bars_branch_list = list(bars_branch)
    if len(bars_branch_list) == 0:
        response_text = "К сожалению, мы пока не можем найти такой адрес."
    else:
        text = ""
        for bar in bars_branch_list:
            ya = "https://yandex.ru/maps/"
            maps_link = f"{ya}?ll={bar.point}&z=16&text={bar.bar.name.replace(' ', '%20')}"
            address = f"<a href='{maps_link}'>{bar.address}</a>"
            address_text = f"📍 {address}"
            text += f"🍻 {bar.barbranch_name}\n{address_text}\n\n{bar.bar.website}\n\n\n"
        response_text = "Сейчас мы знаем о следующих адресах:\n\n" + text

    await update.message.reply_text(
        response_text,
        reply_markup=markup,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    logging_commands(db, update, "bar_branch_list__finish")
    return ConversationHandler.END


handler_bar_branch_list = ConversationHandler(
    entry_points=[CommandHandler("bar_branch_list", choosing_bar)],
    states={
        "step_2": [MessageHandler(filters.TEXT, get_metro_bar_branch)],
        "finish": [MessageHandler(filters.TEXT, bar_branch_list_finish)],
    },
    fallbacks=[],
)
