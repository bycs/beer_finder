import re

from beers.parsers.base import get_html

from bs4 import BeautifulSoup

base_url = "https://we-cidreria.ru"
beer_url = f"{base_url}/menu/beer/"
cidr_url = f"{base_url}/menu/ciders/"


def get_assortment_we_cidreria(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    all_beers = soup.find_all("div", class_="catalog-element-item")
    beer_list = []
    for beer in all_beers:
        name = beer.find("div", class_="catalog-element-name").text
        description = beer.find("p", class_="catalog-element-ru").text
        strength = getattr(beer.find("div", class_="catalog-element-weight"), "text", None)
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
            specifications_dict = {"Крепость": strength}
            beer_list.append(
                {
                    "name": name,
                    "price": price,
                    "description": description,
                    "specifications": specifications_dict,
                }
            )
            new_value = {i["name"]: i for i in beer_list}
            beer_list = list(new_value.values())
    return beer_list


def get_all_we_cidreria():
    all_beers = []
    all_beers += get_assortment_we_cidreria(get_html(beer_url))
    all_beers += get_assortment_we_cidreria(get_html(cidr_url))
    return all_beers
