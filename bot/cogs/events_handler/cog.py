from disnake.ext.commands import Cog, CommandError, MissingPermissions, InteractionBot
from disnake import AllowedMentions, AppCmdInter, Forbidden, Member, Message

from ...services.guilds_settings import get_or_create_guild_settings
from ...services.aiu import send_ai_request
from ...services.prompts import get_greetings_text
from ...services.users.service import get_or_create_user
from ...core.database import session_factory
from ...core.logger import logger
from ...core.embeds import NotEnoughPermissionsEmbed
from ...core.configuration import PERSONALITIES
from ...core.utils import reply_long_message
from .embeds import ActivistRoleAwardedEmbed


class EventsHandlerCog(Cog):
    def __init__(self, bot: InteractionBot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        # TODO: че то сделать с этими соплями
        if message.guild:
            if not message.author.bot:
                async with session_factory() as session:
                    user = await get_or_create_user(
                        session,
                        guild_id=message.guild.id,
                        discord_id=message.author.id,
                    )
                    await session.refresh(user)
                    user.messages_count += 1
                    await session.commit()
                    guild_settings = await get_or_create_guild_settings(session, guild_id=message.guild.id)
                    await session.refresh(guild_settings)
                    if guild_settings.is_activist_role_extraditing and guild_settings.activist_role_messages_count:
                        await session.refresh(user)
                        await session.refresh(guild_settings)
                        if user.messages_count >= guild_settings.activist_role_messages_count:
                            if activist_role := message.guild.get_role(guild_settings.activist_role_id):
                                try:
                                    await message.author.add_roles(activist_role)
                                    await message.channel.send(embed=ActivistRoleAwardedEmbed(member=message.author))
                                except Forbidden:
                                    logger.error("Bot is missing access to award an activist role")

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
                                await message.reply("Ошибка")

    @Cog.listener()
    async def on_slash_command_error(self, inter: AppCmdInter, error: CommandError) -> None:
        if isinstance(error, MissingPermissions):
            logger.info("An attempt to execute an admin command without admin rights.")
            await inter.response.send_message(embed=NotEnoughPermissionsEmbed(), ephemeral=True)
        else:
            raise error

    @Cog.listener()
    async def on_ready(self) -> None:
        logger.info("Bot ready.")

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        async with session_factory() as session:
            guild_settings = await get_or_create_guild_settings(session, guild_id=member.guild.id)
            if guild_settings.is_greetings_enabled:
                if greetings_channel := member.guild.get_channel(guild_settings.greetings_channel_id):
                    await greetings_channel.send(await get_greetings_text(member))


__all__ = ("EventsHandlerCog",)
