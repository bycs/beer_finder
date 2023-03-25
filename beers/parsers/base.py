import random

from dataclasses import dataclass
from typing import Literal

import requests

from beers.decorators import limit_requests
from beers.models.beers import Beer


def clear_text(text: str) -> str:
    """Очистка текста от непечатных символов или знаков форматирования."""
    text = text.replace("\n", "")
    text = text.replace("\r", " ")
    text = text.replace("\xa0", " ")
    text = text.replace("<p>", "")
    text = text.replace("</p>", "")
    text = text.replace("<br>", "")
    text = text.replace("</br>", "")
    text = text.replace("<strong>", "")
    text = text.replace("</strong>", "")
    text = text.replace("&nbsp;", " ")
    text = text.replace("/", " ")
    text = text.replace("  ", " ")
    text = text.strip()
    return text


@limit_requests(random.uniform(4.5, 8.5))
def get_html(url: str) -> str | Literal[False]:
    try:
        result = requests.get(url, verify=False)
        result.raise_for_status()
        return str(result.text)
    except (requests.RequestException, ValueError):
        print(f"Error! Failed to connect to {url}")
        return False


@dataclass
class UnparsedData:
    url: str
    source: str


class BaseBar:
    name: str

    @property
    def urls(self) -> list[str]:
        raise NotImplementedError

    def _get_data(self) -> list[UnparsedData]:
        print(f"Getting {self.__class__.__name__} data from source {self.urls}...")
        return self.get_data()

    def _parse_data(self, unparsed_data: UnparsedData) -> list[dict]:
        print(f"Parsing unparsed_data from {unparsed_data.url}...")
        return self.parse_data(unparsed_data.source)

    def _save_data(self, parsed_data: list[dict]) -> None:
        Beer.objects.sync_bar_beers_to_db(self.name, parsed_data)
        print(f"Save {len(parsed_data)} objects to database from {self.__class__.__name__}")

    def get_data(self) -> list[UnparsedData]:
        result = []
        for url in self.urls:
            source = get_html(url)
            if source:
                data = UnparsedData(url=url, source=source)
                result.append(data)
        return result

    def parse_data(self, unparsed_data: str) -> list[dict]:
        raise NotImplementedError

    def run(self):
        unparsed_data = self._get_data()
        parsed_data = []
        for data in unparsed_data:
            parsed_data += self._parse_data(data)
        self._save_data(parsed_data)
