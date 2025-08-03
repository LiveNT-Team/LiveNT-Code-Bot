"""
The bot configuration

You can find full configuration documentation at `./bot/docs/project_configuration.md.`
"""

from os import getenv
from typing import Literal
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILENAME = BASE_DIR / ".env"

assert load_dotenv(ENV_FILENAME), f"path ENV_FILENAME is not exists"

IS_DEV_MODE = True

LOGGING_FILENAME = BASE_DIR / "bot/logs/logs.log"
LOGGING_FILEMODE: Literal["w", "a"] = "w"

PROD_SQLALCHEMY_URL = f"aiosqlite+sqlite:///./bot/databases/prod_database.db"
DEV_SQLALCHEMY_URL = f"aiosqlite+sqlite:///./bot/databases/dev_database.db"

BOT_TOKEN = getenv("BOT_TOKEN")
