import os
from pytz import timezone

DATABASE_URL = os.getenv(
    "DATABASE_URL", "user=avocado password=avocado dbname=avocado host=localhost"
)
APP_BASE_URL = os.getenv("APP_BASE_URL", "localhost")
ADMIN_SECRET = os.getenv("ADMIN_SECRET", "secret")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")

TIMEZONE = timezone("Europe/Rome")
