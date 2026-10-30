"""Small settings helper. Never print passwords."""
import os
from dotenv import load_dotenv

load_dotenv()

AMAZON = "https://www.amazon.in/"
PARABANK = "https://parabank.parasoft.com/parabank/"
WEBSHOP = "https://demowebshop.tricentis.com/"


def is_live():
    return os.getenv("RUN_LIVE") == "1"


def value(name):
    return os.getenv(name, "").strip()
