__doc__ = """
# Bot Utils

Module contains some useful utilities for services, cogs and core modules
"""

from typing import Generator


def split_into_chunks(text: str, chunk_size: int = 1900) -> Generator[str]:
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]


__all__ = ("reply_long_message",)
