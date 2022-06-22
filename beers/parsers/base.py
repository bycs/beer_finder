import requests


def get_html(url: str) -> str | bool:
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print("Error")
        return False
