import re

from bs4 import BeautifulSoup

url = "https://lambic.ru/beer/"


def get_lambik_data(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    all_beer = soup.find("div", class_="beer-list").find_all("div", class_="beer")
    beer_list = []
    for beer in all_beer:
        name = beer.find("a", class_="beer-link").text

        description = beer.find("div", class_="beer-desc").text
        description = description.replace("\n", "")
        description = description.replace("\r", " ")
        description = description.replace("\xa0", " ")
        description = description.strip()

        specifications = beer.find("div", class_="beer-specifications").text
        specifications = specifications.split("\n")
        specifications_dict = {}
        for specification in specifications:
            if specification:
                specification = specification.split(":")
                specifications_dict[specification[0].strip()] = specification[1].strip()

        price_soup = beer.find("div", class_="beer-price").find_all("li")
        price_list = []
        for price in price_soup:
            size_and_sum = re.findall("[0-9]+", price.text)
            if len(size_and_sum) > 1:
                size = int(size_and_sum[0])
                cost = int(size_and_sum[1])
                price_list.append(int(100 * cost / size * 1000))
            else:
                price = None
                break

        if price_list:
            price = min(price_list)

        beer_list.append(
            {
                "name": name,
                "price": price,
                "description": description,
                "specifications_dict": specifications_dict,
            }
        )

    return beer_list
