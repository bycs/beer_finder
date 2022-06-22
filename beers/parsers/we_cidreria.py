import re

from beers.parsers.base import get_html

from bs4 import BeautifulSoup

base_url_beer = "https://we-cidreria.ru/menu/beer"
base_url_cidr = "https://we-cidreria.ru/menu/ciders"


def get_beers_we_cidreria():
    """Получение данных о пиве."""
    html = get_html(base_url_beer)
    soup = BeautifulSoup(html, "html.parser")
    all_beers = soup.find_all("div", class_="catalog-element-item")
    beer_list = []
    for beer in all_beers:
        name = beer.find("div", class_="catalog-element-name").text
        description = beer.find("p", class_="catalog-element-ru").text
        strenght = beer.find("div", class_="catalog-element-weight").text

        size = beer.find("div", class_="catalog-element-price-item").text
        cost = beer.find("div", class_="catalog-element-price-value").text
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
        else:
            price = None

        specifications_dict = {"Крепость": strenght}
        beer_list.append(
            {
                "name": name,
                "price": price,
                "description": description,
                "specifications": specifications_dict,
            }
        )
    return beer_list
