from disnake.ext.commands import Cog, CommandError, MissingPermissions, InteractionBot
from disnake import AppCmdInter, Member, Message

from ...services.guilds_settings import get_or_create_guild_settings
from ...services.users import get_or_create_user
from ...services.prompts import get_greetings_text
from ...core.database import session_factory
from ...core.logger import logger
from ...core.embeds import NotEnoughPermissionsEmbed
from ...cogs.stats import StatsCog
from ...cogs.ai import AICog


class EventsHandlerCog(Cog):
    def __init__(self, bot: InteractionBot):
        super().__init__()
        self.bot = bot

    @Cog.listener()
    async def on_slash_command_error(
        self, inter: AppCmdInter, error: CommandError
    ) -> None:
        if isinstance(error, MissingPermissions):
            logger.info("An attempt to execute an admin command without admin rights.")
            await inter.response.send_message(
                embed=NotEnoughPermissionsEmbed(), ephemeral=True
            )
        else:
            raise error

    @Cog.listener()
    async def on_ready(self) -> None:
        logger.info("Bot ready.")

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        async with session_factory() as session:
            guild_settings = await get_or_create_guild_settings(
                session, guild_id=member.guild.id
            )
            if guild_settings.is_greetings_enabled:
                if greetings_channel := member.guild.get_channel(
                    guild_settings.greetings_channel_id
                ):
                    await greetings_channel.send(await get_greetings_text(member))

    @Cog.listener()
    async def on_message(self, message: Message):
        async with session_factory() as session:
            # Вызываем всё в одном месте чтобы не было проблем с тем что в бд одновременно поступают запросы на создание пользователя
            if not message.author.bot:
                guild_settings = await get_or_create_guild_settings(
                    session,
                    guild_id=message.guild.id,
                )
                author_user_model = await get_or_create_user(
                    session,
                    guild_id=message.guild.id,
                    discord_id=message.author.id,
                )
                await StatsCog.handle_message(
                    session=session,
                    message=message,
                    guild_settings=guild_settings,
                    author_user_model=author_user_model,
                )
                await AICog.handle_message(
                    bot=self.bot,
                    session=session,
                    message=message,
                    guild_settings=guild_settings,
                    author_user_model=author_user_model,
                )


__all__ = ("EventsHandlerCog",)
