__doc__ = """
# Bot Utils

Module contains some useful utilities for services, cogs and core modules
"""

from disnake import AllowedMentions, TextChannel
from ..core.logger import logger


async def send_long_message(channel: TextChannel, message: str) -> None:
    for i in range(0, len(message), 1900):
        logger.info(message)
        await channel.send(
            message[i : i + 1900],
            allowed_mentions=AllowedMentions(
                everyone=False,
                users=False,
            ),
        )


__all__ = ("send_long_message",)
