import re

from beers.parsers.base import clear_text, get_html

from bs4 import BeautifulSoup

base_url = "https://lambic.ru"
list_urls_for_parce = ["/beer/draft"]


def get_urls_list_lambic(html: str) -> list:
    """Получение списка ссылок на различные сорта пива."""
    soup = BeautifulSoup(html, "html.parser")
    all_urls = soup.find("ul", class_="contentmenu-list").find_all("li", class_="contentmenu-item")
    urls_list = []
    for url_item in all_urls[1:]:
        urls_list.append(url_item.find("a")["href"])
    return urls_list


def get_data_lambic(html: str) -> list:
    """Получение данных о пиве."""
    soup = BeautifulSoup(html, "html.parser")
    all_beer = soup.find("div", class_="beer-list").find_all("div", class_="beer")
    beer_list = []
    for beer in all_beer:
        name = beer.find("a", class_="beer-link").text

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


def get_all_beers_lambic(base_url: str, list_urls_for_parce: list) -> list:
    """Получение данных о всем пиве."""
    html = get_html(f"{base_url}{list_urls_for_parce[0]}")
    all_beers = []
    list_urls_for_parce = get_urls_list_lambic(html)
    all_beers += get_data_lambic(html)
    for url in list_urls_for_parce:
        html = get_html(f"{base_url}{url}")
        all_beers += get_data_lambic(html)
    return all_beers
