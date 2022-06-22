import requests


def get_html(url: str) -> str | bool:
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        print("Error")
        return False


def clear_text(text: str) -> str:
    """Очистка текста от непечатных символов или знаков форматирования."""
    text = text.replace("\n", "")
    text = text.replace("\r", " ")
    text = text.replace("\xa0", " ")
    text = text.replace("  ", " ")
    text = text.strip()
    return text
