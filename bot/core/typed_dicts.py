from typing import TypedDict


class Personality(TypedDict):
    name: str
    description: str
    temperature: float
    max_tokens: int


__all__ = ("Personality",)
