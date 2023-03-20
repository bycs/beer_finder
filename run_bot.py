import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()


if __name__ == "__main__":
    from bot.bot import run_bot

    run_bot()
