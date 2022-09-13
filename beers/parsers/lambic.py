import re

from bs4 import BeautifulSoup

from beers.parsers.base import BaseBar
from beers.parsers.base import clear_text
from beers.parsers.base import get_html


class Lambic(BaseBar):
    name = "Lambic"

    @property
    def urls(self) -> list[str]:
        base_url = "https://lambic.ru"
        urls = ["https://lambic.ru/beer/draft"]
        html = get_html(urls[0])
        soup = BeautifulSoup(html, "html.parser")
        all_urls = soup.find("ul", class_="contentmenu-list").find_all(
            "li", class_="contentmenu-item"
        )
        for url_item in all_urls[1:]:
            url = url_item.find("a")["href"]
            urls.append(f"{base_url}{url}")
        return urls

    def parse_data(self, unparsed_data: str):
        soup = BeautifulSoup(unparsed_data, "html.parser")
        all_beer = soup.find("div", class_="beer-list").find_all("div", class_="beer")
        beer_list = []
        for beer in all_beer:
            name = beer.find("a", class_="beer-link").text.strip()

            description = beer.find("div", class_="beer-desc").text
            description = clear_text(description)

            category = soup.find("li", class_="contentmenu-item is-active").text

            specifications = beer.find("div", class_="beer-specifications").text
            specifications = specifications.split("\n")
            specifications_dict = {"Категория": category.capitalize()}
            for specification in specifications:
                if specification:
                    specification = specification.split(":")
                    specifications_dict[specification[0].strip()] = specification[1].strip()

            price_soup = beer.find("div", class_="beer-price").find_all("li")
            price_list = []
            for price in price_soup:
                size_and_cost = re.findall(r"\d+", price.text)
                if len(size_and_cost) > 1:
                    size = int(size_and_cost[0])
                    cost = int(size_and_cost[1])
                    price_list.append(int(100 * cost / size * 1000))

            if price_list:
                price = min(price_list)
            else:
                price = None

            beer_list.append(
                {
                    "name": name,
                    "price": price,
                    "description": description,
                    "specifications": specifications_dict,
                }
            )

        return beer_list
