import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "tienda",
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "abarrotes_api.urls"

WSGI_APPLICATION = "abarrotes_api.wsgi.application"

# ---------- Base de datos MySQL ----------
# Primero ejecuta base_datos.sql en MySQL Workbench.
# Cambia USER y PASSWORD por los de tu MySQL.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "abarrotes",
        "USER": "root",
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": "localhost",
        "PORT": "3306",
    }
}


DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
