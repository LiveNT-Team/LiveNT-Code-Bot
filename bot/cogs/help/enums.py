from enum import StrEnum, auto


class HelpMenuSectionsEnum(StrEnum):
    AI = auto()
    PERSONALITIES = auto()
    SETTINGS = auto()
    STATS = auto()


__all__ = ("HelpMenuSectionsEnum",)
