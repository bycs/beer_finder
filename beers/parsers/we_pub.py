import re

from beers.parsers.base import BaseBar, clear_text

from bs4 import BeautifulSoup


class WePub(BaseBar):
    name = "WE Pub"
    urls = ["https://we-pub.ru/beer/"]

    def parse_data(self, unparsed_data: str):
        soup = BeautifulSoup(unparsed_data, "html.parser")
        soup = soup.find("div", class_="catalog-element-list")
        all_category = soup.find_all("div", class_="catalog-element-section-name")
        all_beers = soup.find_all("div", class_="catalog-element-section-list")
        beer_list = []
        for i in range(len(all_category)):
            category = all_category[i].text
            specifications_dict = {"Категория": category.capitalize()}
            beers = all_beers[i].find_all("div", class_="catalog-element-item")
            for beer in beers:
                name = beer.find("div", class_="catalog-element-name").text
                name = clear_text(name)
                description = beer.find("div", class_="catalog-element-desc").text
                other_info = description.split(". ")[-1]
                other_info = other_info.split(".,")
                if len(other_info) > 1:
                    strenght = other_info[0]
                    specifications_dict["Крепость"] = strenght
                    other_info = other_info[1].split(",")
                    if len(other_info) > 1:
                        brewery = other_info[0].strip()
                        country = other_info[1].strip()
                        specifications_dict["Изготовитель"] = brewery
                        specifications_dict["Страна"] = country

                size = beer.find("div", class_="catalog-element-weight").text
                size = size.replace("мл", "")
                size = float(size.replace(",", "."))
                cost = beer.find("div", class_="catalog-element-price").text
                cost = int(re.findall(r"\d+", cost)[0])
                price = int(100 * cost / size)

                if 0.3 <= size < 3:
                    beer_list.append(
                        {
                            "name": name,
                            "price": price,
                            "description": description,
                            "specifications": specifications_dict,
                        }
                    )

        return beer_list
