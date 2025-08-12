"""
The bot configuration

You can find full configuration documentation at `./bot/docs/project_configuration.md.`
"""

import logging
from os import getenv
from typing import Literal, Sequence
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILENAME = BASE_DIR / ".env"

assert load_dotenv(ENV_FILENAME), f"path ENV_FILENAME is not exists"

IS_DEV_MODE = True

LOGGING_FILENAME = BASE_DIR / "bot/logs/logs.log"
LOGGING_FILEMODE: Literal["w", "a"] = "w"
LOGGING_LEVEL: Literal[10, 20, 30, 40, 50] = logging.INFO
LOGGING_FORMAT: str = "%(asctime)s [%(levelname)s] %(message)s"
LOGGING_DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

PROD_SQLALCHEMY_URL = f"sqlite+aiosqlite:///./bot/databases/prod_database.db"
DEV_SQLALCHEMY_URL = f"sqlite+aiosqlite:///./bot/databases/dev_database.db"

TEST_GUILDS: Sequence[int] = {1401173801689022517}

BOT_TOKEN = getenv("BOT_TOKEN")
