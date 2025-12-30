from logging import FileHandler, StreamHandler, getLogger, basicConfig

from .configuration import (
    LOGGING_FILEMODE,
    LOGGING_FILENAME,
    LOGGING_LEVEL,
    LOGGING_FORMAT,
    LOGGING_DATETIME_FORMAT,
)

logger = getLogger(__name__)
basicConfig(
    format=LOGGING_FORMAT,
    datefmt=LOGGING_DATETIME_FORMAT,
    level=LOGGING_LEVEL,
    handlers=[
        StreamHandler(),
        FileHandler(
            filename=LOGGING_FILENAME,
            mode=LOGGING_FILEMODE,
            encoding="utf-8",
        ),
    ],
)

__all__ = ("logger",)
