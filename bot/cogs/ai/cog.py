from disnake.ext.commands import Cog, Param, slash_command, String, InteractionBot
from disnake import AppCmdInter, Message


from .embeds import AIErrorEmbed, AIIsDisabledEmbed
from ...services.aiu import send_ai_request
from ...services.users import get_or_create_user
from ...services.guilds_settings import get_or_create_guild_settings
from ...core.configuration import PERSONALITIES
from ...core.database import session_factory
from ...core.utils import reply_long_message


class AICog(Cog):
    def __init__(self, bot: InteractionBot):
        super().__init__()
        self.bot = bot

    @slash_command()
    async def ask(
        self,
        inter: AppCmdInter,
        text: String[str, 3, 200],
        personality_name: str | None = Param(default=None, choices=list(PERSONALITIES.keys())),
    ) -> None:
        await inter.response.defer()
        async with session_factory() as session:
            guild_settings = await get_or_create_guild_settings(session, guild_id=inter.guild.id)
            await session.refresh(guild_settings)
            if guild_settings.is_ai_enabled:
                if personality_name:
                    if ai_response := await send_ai_request(text=text, personality=PERSONALITIES[personality_name]):
                        await reply_long_message(ai_response, inter=inter)
                    else:
                        await inter.edit_original_response(embed=AIErrorEmbed())
                else:
                    user = await get_or_create_user(
                        session,
                        discord_id=inter.author.id,
                        guild_id=inter.guild.id,
                    )
                    await session.refresh(user)
                    if ai_response := await send_ai_request(text=text, personality=PERSONALITIES[user.current_personality_name]):
                        await reply_long_message(ai_response, inter=inter)
                    else:
                        await inter.edit_original_response(embed=AIErrorEmbed())
            else:
                await inter.edit_original_response(embed=AIIsDisabledEmbed())

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.guild:
            if not message.author.bot:
                async with session_factory() as session:
                    guild_settings = await get_or_create_guild_settings(session, guild_id=message.guild.id)
                    if self.bot.user in message.mentions or message.channel.id == guild_settings.ai_channel_id:
                        if guild_settings.is_ai_enabled:
                            user = await get_or_create_user(
                                session,
                                guild_id=message.guild.id,
                                discord_id=message.author.id,
                            )
                            if ai_response := await send_ai_request(text=message.content, personality=PERSONALITIES[user.current_personality_name]):
                                await reply_long_message(ai_response, message_to_reply=message)
                            else:
                                await message.reply(embed=AIErrorEmbed())


__all__ = ("AICog",)
