from disnake.ext.commands import Cog, CommandError, MissingPermissions, InteractionBot
from disnake import AllowedMentions, AppCmdInter, Member, Message

from ...services.guilds_settings import get_or_create_guild_settings
from ...services.aiu import send_ai_request
from ...services.prompts import get_greetings_text
from ...services.users.service import get_or_create_user
from ...core.database import session_factory
from ...core.logger import logger
from ...core.embeds import NotEnoughPermissionsEmbed
from ...core.configuration import PERSONALITIES


class EventsHandlerCog(Cog):
    def __init__(self, bot: InteractionBot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
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
                    logger.info("Messages received, message counter increased.")

                    if self.bot.user in message.mentions or message.channel.id == guild_settings.ai_channel_id:
                        guild_settings = await get_or_create_guild_settings(session, guild_id=message.guild.id)
                        if guild_settings.is_ai_enabled:
                            user = await get_or_create_user(
                                session,
                                guild_id=message.guild.id,
                                discord_id=message.author.id,
                            )
                            if ai_response := await send_ai_request(text=message.content, personality=PERSONALITIES[user.current_personality_name]):
                                await message.channel.send(
                                    content=ai_response,
                                    allowed_mentions=AllowedMentions(
                                        everyone=False,
                                        users=False,
                                    ),
                                )
                            else:
                                await message.channel.send("Ошибка")

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
        greeting_text = await get_greetings_text(member)
        logger.info(greeting_text)
        
        # Отправка в системный канал (если настроен)
        if member.guild.system_channel:
            await member.guild.system_channel.send(greeting_text)


__all__ = ("EventsHandlerCog",)
