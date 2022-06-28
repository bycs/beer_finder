import re

from beers.parsers.base import get_html

from bs4 import BeautifulSoup

base_url_beer = "https://we-pub.ru/beer/"


def get_beers_we_pub():
    """Получение данных о пиве."""
    html = get_html(base_url_beer)
    soup = BeautifulSoup(html, "html.parser")
    all_beers = soup.find_all("div", class_="catalog-element-item")
    beer_list = []
    for beer in all_beers:
        name = beer.find("div", class_="catalog-element-name").text.replace("/", "").strip()
        description = beer.find("div", class_="catalog-element-desc").text
        size = beer.find("div", class_="catalog-element-weight").text
        cost = beer.find("div", class_="catalog-element-price").text
        size = re.findall(r"\d+,\d+", size)
        cost = re.findall(r"\d+", cost)
        price_list = []
        for i in range(len(size)):
            cost_item = int(cost[i])
            size_item = float(size[i].replace(",", "."))
            price_item = int(100 * cost_item / size_item)
            price_list.append(price_item)

        if price_list:
            price = min(price_list)
        if size_item > 0.3:
            price_list.append(price_item)
        else:
            price = None
        beer_list.append(
            {
                "name": name,
                "price": price,
                "description": description,
            }
        )
        for i in range(len(beer_list)):
            if beer_list[i]["price"] is None:
                del beer_list[i]

    return beer_list
