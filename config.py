import os

from dotenv import dotenv_values
from dotenv import load_dotenv


config = dotenv_values(".env")

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DEBUG = int(os.getenv("DEBUG", 0))

DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DJANGO_ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost").split(" ")
DJANGO_CSRF_TRUSTED_ORIGINS = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "localhost").split(" ")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "pass")
DB_NAME = os.getenv("DB_NAME", "db")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GRAPHHOPPER_KEY = os.getenv("GRAPHHOPPER_KEY")
YANDEXMAP_KEY = os.getenv("YANDEXMAP_KEY")
