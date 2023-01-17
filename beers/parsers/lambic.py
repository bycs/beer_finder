import random
import re

from bs4 import BeautifulSoup

from beers.parsers.base import BaseBar
from beers.parsers.base import clear_text
from beers.parsers.base import get_html
from beers.parsers.base import limit_requests


class Lambic(BaseBar):
    name = "Lambic"

    @property
    def urls(self) -> list[str]:
        base_url = "https://lambic.ru"
        start_url = "https://lambic.ru/beer/draft/"
        beer_urls = []
        html = get_html(start_url)
        soup = BeautifulSoup(html, "html.parser")
        beer_items = soup.select("*[class^='BeerSearch_beerItems']")
        beers = beer_items[0].find_all("a")

        for beer in beers:
            url = beer.get("href")
            beer_urls.append(f"{base_url}{url}")
        return beer_urls

    @staticmethod
    def get_beer_name(soup: BeautifulSoup) -> str:
        return str(soup.select("*[class^='BeerPage_title']")[0].text)

    @staticmethod
    def get_beer_price(soup: BeautifulSoup) -> int | None:
        price_list = []
        price_raw = soup.select("*[class^='BeerPage_priceDiv']")
        for price in price_raw:
            size_and_cost = re.findall(r"\d+", price.text)
            if len(size_and_cost) > 1:
                cost = int(size_and_cost[0])
                size = int(size_and_cost[1])
                price_list.append(int(100 * cost / size * 1000))
        if price_list:
            return min(price_list)
        else:
            return None

    @staticmethod
    def get_beer_description(soup: BeautifulSoup) -> str:
        description = ""
        try:
            description_raw = soup.select("*[class^='BeerPage_descriptionText']")[0].text
            description = clear_text(description_raw)
        except IndexError:
            print("Description not found!")
        return clear_text(description)

    @staticmethod
    def get_beer_specifications(soup: BeautifulSoup) -> dict | None:
        specifications_dict = {}
        try:
            specifications_raw = soup.select("*[class^='BeerPage_specifications']")[0]
            specifications_raw = list(specifications_raw.find_all("p"))
            for i, spec in enumerate(specifications_raw, start=1):
                if i % 2:
                    specifications_dict[spec.text] = specifications_raw[i].text
        except IndexError:
            print("Specifications not found!")
        return specifications_dict

    @limit_requests(random.uniform(0.5, 3.5))
    def parse_data(self, unparsed_data: str) -> list[dict]:
        soup = BeautifulSoup(unparsed_data, "html.parser")

        return [
            {
                "name": self.get_beer_name(soup),
                "price": self.get_beer_price(soup),
                "description": self.get_beer_description(soup),
                "specifications": self.get_beer_specifications(soup),
            }
        ]
