from disnake.ext.commands import Cog, Param, slash_command, InteractionBot
from disnake import AppCmdInter, Attachment, Message, TextChannel

from core.base_embeds import SuccessEmbed
from core.utils import split_into_chunks
from core.configuration import PERSONALITIES
from cogs.settings.decorators import has_developer_role
from services.mysqliup.service import MySqliUp
from services.guilds.service import set_guild_setting, get_guild
from services.aiu.service import send_ai_request
from services.users.service import get_or_create_user


class AIChat(Cog):
    def __init__(self, bot: InteractionBot):
        super().__init__()
        self.bot = bot

    @slash_command()
    @has_developer_role
    async def enable_ai_chat(self, inter: AppCmdInter) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(db, inter.guild_id, "ai_chat_enabled", True)
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def disable_ai_chat(self, inter: AppCmdInter) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(db, inter.guild_id, "ai_chat_enabled", False)
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())

    @slash_command()
    @has_developer_role
    async def set_ai_channel(
        self,
        inter: AppCmdInter,
        channel: TextChannel | None = Param(
            None,
            description="Если пустое - сбросить",
        ),
    ) -> None:
        db = MySqliUp()
        await db.connect()
        await db.begin()
        await set_guild_setting(
            db,
            inter.guild_id,
            "ai_channel_id",
            channel.id if channel else None,
        )
        await db.commit()
        await db.close()
        await inter.response.send_message(embed=SuccessEmbed())

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        async with MySqliUp() as db:
            if message.author.bot:
                return
            await db.connect()
            guild = await get_guild(db, message.guild.id)
            if not guild:
                return
            if not guild["ai_chat_enabled"]:
                return
            if (
                message.channel.id == guild["ai_channel_id"]
                or self.bot.user in message.mentions
            ):
                user = await get_or_create_user(db, message.guild.id, message.author.id)
                images: list[Attachment] = list(
                    filter(
                        lambda attachment: attachment.content_type
                        in {
                            "image/png",
                            "image/jpeg",
                            "image/gif",
                            "image/webp",
                        },
                        message.attachments,
                    )
                )
                response = await send_ai_request(
                    message.content,
                    PERSONALITIES[user["ai_per_name"]],
                    images[0].url if images else None,
                )
                for number, chunk in enumerate(split_into_chunks(response)):
                    if number == 0:
                        await message.reply(chunk)
                    else:
                        await message.channel.send(chunk)


__all__ = ("AIChat",)
