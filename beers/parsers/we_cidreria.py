import re

from beers.parsers.base import get_html

from bs4 import BeautifulSoup


def get_beers_cidreria():
    """Получение данных о пиве."""
    html = get_html("https://we-cidreria.ru/menu/beer")
    soup = BeautifulSoup(html, "html.parser")
    all_beer = soup.find("div", class_="catalog-element-list").find_all(
        "div", class_="catalog-element-item"
    )
    beer_list = []
    for beer in all_beer:
        name = beer.find("div", class_="catalog-element-name").text
        description = beer.find("p", class_="catalog-element-ru").text
        strenght = beer.find("div", class_="catalog-element-weight").text

        price_soup = beer.find("div", class_="catalog-element-price-value").text
        price_list = []
        price_soup = price_soup.replace("\n", "")
        price_soup = price_soup.replace("/", " ")
        price_soup = price_soup.replace("Р", "")
        for price in price_soup:
            sums = re.findall("[0-9]+", price_soup)
            if len(sums) >= 1:
                sum1 = int(sums[0])
                price_list.append(int((sum1 * 2) * 1000))
            else:
                price_soup = None
                break

        if price_list:
            price_soup = min(price_list)

        beer_list.append(
            {
                "name": name,
                "price": price_soup,
                "description": description,
                "strenght": strenght,
            }
        )

    return beer_list
