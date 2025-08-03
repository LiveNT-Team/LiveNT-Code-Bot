"""
The bot configuration template

You can find full configuration documentation at `./bot/docs/project_configuration.md.`
"""

from os import getenv
from typing import Literal
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILENAME = BASE_DIR / ".env"

assert load_dotenv(ENV_FILENAME), f"path ENV_FILENAME' is not exists"

DEV = True

LOGGING_FILENAME = BASE_DIR / "logs/logs.log"
LOGGING_FILEMODE: Literal["w", "a"] = "w"

PROD_DATABASE_FILENAME = BASE_DIR / "product_sqlite3.db"
DEV_DATABASE_FILENAME = BASE_DIR / "dev_sqlite3.db"
SQLALCHEMY_URL = f"sqlite:///{DEV_DATABASE_FILENAME if DEV else PROD_DATABASE_FILENAME}"

BOT_TOKEN = getenv("BOT_TOKEN")
