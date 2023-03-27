from bot.db import db
from bot.db import get_number_unique_users
from bot.db import get_number_use_command


def get_number_use_command_text() -> str:
    commands = get_number_use_command(db)
    if commands is None:
        return "История вызовов команд не обнаружена"

    text = "Количество вызовов команд:\n"
    for command, count in commands.items():
        text += f"\n/{command} вызывали {count} раз"
    return text


def get_number_unique_users_text() -> str:
    number_unique_users = get_number_unique_users(db)
    text = f"Количество уникальных пользователей: {number_unique_users}"
    return text
