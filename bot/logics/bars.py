from collections import Counter
from operator import itemgetter

from aiogram import Dispatcher
from aiogram import md
from aiogram import types
from aiogram.dispatcher import FSMContext

from beers.logics.geo import Point
from beers.logics.geo import YandexMapGeo
from beers.logics.geo import get_distance
from beers.logics.utils import get_bars
from beers.logics.utils import get_bars_branches
from bot.forms import AddressForm
from bot.forms import GeoBarForm
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


class BarBranchList(BaseLogic):
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
            metro_list = list(set(metro_list))
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
                    ya = "https://yandex.ru/maps/"
                    maps_link = f"{ya}?ll={bar.point}&z=16&text={bar.bar.name.replace(' ', '%20')}"
                    address = md.hlink(bar.address, maps_link)
                    address_text = f"📍 {address}"
                    text += f"🍻 {bar.barbranch_name}\n{address_text}\n\n{bar.bar.website}\n\n\n"
                response_text = "Сейчас мы знаем о следующих адресах:\n\n" + text

            await message.reply(
                response_text,
                reply_markup=markup,
                parse_mode="HTML",
                disable_web_page_preview=True,
            )

        await state.finish()


class BarBranchGeo(BaseLogic):
    def _register(self, dp: Dispatcher) -> None:
        dp.register_message_handler(self.geo_bar_start, commands="geo_bar")
        dp.register_message_handler(self.geo_bar_step2, state=GeoBarForm.bar)
        dp.register_message_handler(
            self.geo_bar_finish,
            state=GeoBarForm.search_type,
            content_types=types.ContentTypes.LOCATION | types.ContentTypes.TEXT,
        )

    @staticmethod
    async def geo_bar_start(message: types.Message) -> None:
        await GeoBarForm.bar.set()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        bars = get_bars().values_list("name", flat=True)
        markup.add(*bars)
        markup.add("Любой бар")

        await message.reply("Выбери бар (кнопкой)", reply_markup=markup)

    @staticmethod
    async def geo_bar_step2(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            if message.text == "Любой бар":
                data["bar"] = None
            else:
                data["bar"] = message.text
            await GeoBarForm.next()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            button_geo = types.KeyboardButton("📍 Отправить геопозицию", request_location=True)
            markup.add(button_geo)
            await message.reply("Отправьте геопозицию или введите адрес", reply_markup=markup)

    @staticmethod
    async def geo_bar_finish(message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            if message.location:
                data["search_type"] = "location"
                location_user = Point(message.location.longitude, message.location.latitude)

            else:
                data["search_type"] = "address"
                geo = YandexMapGeo()
                point = geo.geocode(message.text)
                if point:
                    location_user = point

            bars_branch = get_bars_branches(data["bar"])
            markup = types.ReplyKeyboardRemove()
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
                    address = md.hlink(bar.address, maps_link)
                    address_text = f"📍 {address}\n\n"
                    name_text = f"🍻 {bar.barbranch_name} ~{distances_sorted[bar]} км\n"
                    website_text = f"{bar.bar.website}\n\n\n"
                    text += name_text + address_text + website_text
                response_text = "Самые близкие бары:\n\n" + text

            await message.reply(
                response_text,
                reply_markup=markup,
                parse_mode="HTML",
                disable_web_page_preview=True,
            )

        await state.finish()
