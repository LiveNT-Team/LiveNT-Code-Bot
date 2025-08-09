"""
The module provides some base embeds classes, ErrorEmbed, SuccessEmbed, WarningEmbed, InfoEmbed.
"""

from disnake import Embed, Color
from datetime import datetime


class TimestampEmbed(Embed):
    def __init__(
        self,
        *,
        title=None,
        type="rich",
        description=None,
        url=None,
        timestamp=datetime.now(),
        color=None,
    ):
        super().__init__(
            title=title,
            type=type,
            description=description,
            url=url,
            timestamp=timestamp,
            color=color,
        )


class ErrorEmbed(TimestampEmbed):
    def __init__(
        self,
        *,
        type="rich",
        description=None,
        url=None,
    ):
        super().__init__(
            title="Ошибка",
            type=type,
            description=description,
            url=url,
            color=Color.red(),
        )


class CriticalErrorEmbed(TimestampEmbed):
    def __init__(
        self,
        *,
        type="rich",
        description=None,
        url=None,
    ):
        super().__init__(
            title="Критическая ошибка",
            type=type,
            description=description,
            url=url,
            color=Color.red(),
        )


class SuccessEmbed(TimestampEmbed):
    def __init__(
        self,
        *,
        type="rich",
        description=None,
        url=None,
    ):
        super().__init__(
            title="Успешно",
            type=type,
            description=description,
            url=url,
            color=Color.green(),
        )


class WarningEmbed(TimestampEmbed):
    def __init__(
        self,
        *,
        type="rich",
        description=None,
        url=None,
    ):
        super().__init__(
            title="Предупреждение",
            type=type,
            description=description,
            url=url,
            color=Color.yellow,
        )


class InfoEmbed(TimestampEmbed):
    def __init__(
        self,
        *,
        type="rich",
        description=None,
        url=None,
    ):
        super().__init__(
            title="Информация",
            type=type,
            description=description,
            url=url,
            color=Color.blue(),
        )


__all__ = (
    "ErrorEmbed",
    "SuccessEmbed",
    "WarningEmbed",
    "InfoEmbed",
    "CriticalErrorEmbed",
    "TimestampEmbed",
)
