"""
The bot configuration

You can find full configuration documentation at `./bot/docs/project_configuration.md.`
"""

import logging
from os import getenv
from typing import Literal, Sequence
from pathlib import Path

from .typed_dicts import Personality


BASE_DIR = Path(__file__).resolve().parent.parent

IS_DEV_MODE = False

LOGGING_FILENAME = BASE_DIR / "logs/logs.log"
LOGGING_FILEMODE: Literal["w", "a"] = "w"
LOGGING_LEVEL: Literal[10, 20, 30, 40, 50] = logging.INFO
LOGGING_FORMAT: str = "%(asctime)s [%(levelname)s] %(message)s"
LOGGING_DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

MYSQL_DATABASE = getenv("MYSQL_DATABASE")
MYSQL_PASSWORD = getenv("MYSQL_PASSWORD")
MYSQL_USERNAME = getenv("MYSQL_USERNAME")
MYSQL_HOST = getenv("MYSQL_HOST")

DEV_MYSQL_DATABASE = getenv("DEV_MYSQL_DATABASE")
DEV_MYSQL_PASSWORD = getenv("DEV_MYSQL_PASSWORD")
DEV_MYSQL_USERNAME = getenv("DEV_MYSQL_USERNAME")
DEV_MYSQL_HOST = getenv("DEV_MYSQL_HOST")

TEST_GUILDS: Sequence[int] = getenv("TEST_GUILDS").rstrip().split(",")

BOT_TOKEN = getenv("BOT_TOKEN")

AI_API_URL = getenv("AI_API_URL")
AI_API_KEY = getenv("AI_API_KEY")

DEFAULT_PERSONALITY_NAME: str = "assistant"
PERSONALITIES: dict[str, Personality] = {
    "assistant": Personality(
        name="Ассистент",
        description="Будь лаконичным и полезным. Только суть.",
        temperature=0.7,
        max_tokens=1000,
    ),
    "warm": Personality(
        name="Теплый помощник",
        description="Отвечай тепло и с пониманием. Кратко, но с заботой.",
        temperature=0.8,
        max_tokens=1200,
    ),
    "ideas": Personality(
        name="Генератор идей",
        description="Думай нестандартно. Предлагай яркие и свежие идеи.",
        temperature=0.9,
        max_tokens=1500,
    ),
    "consultant": Personality(
        name="Консультант",
        description="Будь точным. Отвечай как эксперт, без воды.",
        temperature=0.3,
        max_tokens=800,
    ),
    "programmer": Personality(
        name="Программист",
        description="Отвечай как опытный разработчик. Четко, по делу, с примерами.",
        temperature=0.4,
        max_tokens=1200,
    ),
    "explorer": Personality(
        name="Исследователь",
        description="Исследуй тему глубоко. Задавай уточняющие вопросы. Отвечай с интересом и стремлением к пониманию.",
        temperature=0.7,
        max_tokens=1500,
    ),
}
