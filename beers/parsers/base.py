from beers.models.beers import Beer

import requests


def clear_text(text: str) -> str:
    """Очистка текста от непечатных символов или знаков форматирования."""
    text = text.replace("\n", "")
    text = text.replace("\r", " ")
    text = text.replace("\xa0", " ")
    text = text.replace("/", " ")
    text = text.replace("  ", " ")
    text = text.strip()
    return text


def get_html(url) -> str | bool:
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print("Error")
        return False


class BaseBar:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def _get_data(self):
        print(f"Getting {self.__class__.__name__} data from source {self.url}...")
        return self.get_data()

    def _parse_data(self, unparsed_data: str):
        print("Parsing unparsed_data...")
        return self.parse_data(unparsed_data)

    def _save_data(self, parsed_data):
        Beer.beer_managers.sync_bar_beers_to_db(self.name, parsed_data)
        print(f"Save data {parsed_data} to database from {self.__class__.__name__}")

    def get_data(self) -> str | bool:
        try:
            result = requests.get(self.url)
            result.raise_for_status()
            return result.text
        except (requests.RequestException, ValueError):
            print("Error")
            return False

    def parse_data(self, unparsed_data: str):
        raise NotImplementedError

    def run(self):
        unparsed_data = self._get_data()
        parsed_data = self._parse_data(unparsed_data)
        self._save_data(parsed_data)
