import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = int(os.getenv("DEBUG", 0))
DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DJANGO_ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost").split(" ")
DJANGO_CSRF_TRUSTED_ORIGINS = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "localhost").split(" ")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "pass")
DB_NAME = os.getenv("DB_NAME", "db")
