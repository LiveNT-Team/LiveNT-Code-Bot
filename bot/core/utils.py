__doc__ = """
# Bot Utils

Module contains some useful utilities for services, cogs and core modules
"""

from disnake import AllowedMentions, AppCmdInter, Message
from ..core.logger import logger


async def reply_long_message(
    text: str,
    message_to_reply: Message | None = None,
    inter: AppCmdInter | None = None,
    allowed_mentions: AllowedMentions = AllowedMentions(
        everyone=False,
        users=False,
    ),
) -> None:
    for i in range(0, len(text), 1900):
        if inter:
            await inter.edit_original_response(
                text[i : i + 1900],
                allowed_mentions=allowed_mentions,
            )
        elif message_to_reply:
            await message_to_reply.reply(
                text[i : i + 1900],
                allowed_mentions=allowed_mentions,
            )
        else:
            raise ValueError("'message_to_reply' and 'inter' are None")


__all__ = ("reply_long_message",)
