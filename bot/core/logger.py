"""
Module contains `logger` object to interact with bot logs
"""

from logging import FileHandler, StreamHandler, getLogger, basicConfig

logger = getLogger(__name__)
basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        StreamHandler(),
        FileHandler(
            filename="",
            mode="w",
            encoding="utf-8",
        ),
    ],
)

__all__ = ("logger",)
