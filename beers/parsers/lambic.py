import random
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from beers.parsers.base import BaseBar
from beers.parsers.base import clear_text
from beers.parsers.base import limit_requests


options = Options()
options.add_argument("--headless")


class Lambic(BaseBar):
    name = "Lambic"

    @property
    def urls(self) -> list[str]:
        start_url = "https://lambic.ru/sitemap"
        with webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        ) as browser:
            browser.get(start_url)
            browser.implicitly_wait(random.uniform(2.5, 6.5))
            confirm_age(browser=browser)

            links = browser.find_elements(By.CSS_SELECTOR, "a")
            re_beer = re.compile(r"^.*\/beer\/\S+\/\S+$")
            links_beer = [
                link.get_attribute("href")
                for link in links
                if re_beer.match(link.get_attribute("href"))
            ]

            re_category = re.compile(r"^.*\/beer\/[0-9a-zA-Z-]+$")
            links_category = [  # noqa: F841
                link.get_attribute("href")
                for link in links
                if re_category.match(link.get_attribute("href"))
            ]
            return links_beer

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
                    specifications_dict[spec.text.capitalize()] = specifications_raw[
                        i
                    ].text.capitalize()
        except IndexError:
            print("Specifications not found!")
        return specifications_dict

    @limit_requests(random.uniform(4.5, 8.5))
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


def confirm_age(browser: webdriver.Chrome) -> None:
    """Подтверждение возраста"""
    try:
        browser.find_element(By.CLASS_NAME, "age-confirm-btn").click()
    except NoSuchElementException:
        pass
