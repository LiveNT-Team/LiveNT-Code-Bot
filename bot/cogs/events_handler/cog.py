from disnake.ext.commands import Cog, InteractionBot, MissingPermissions
from disnake import AppCmdInter, Member

from core.logger import logger
from core.embeds import NotEnoughPermissionsEmbed
from services.mysqliup.service import MySqliUp
from services.guilds.service import get_guild
from services.prompts.service import get_greetings_text


class EventsHandlerCog(Cog):
    @Cog.listener()
    async def on_ready() -> None:
        logger.info("Bot is ready")

    @Cog.listener()
    async def on_slash_command_error(inter: AppCmdInter, error: Exception):
        if isinstance(error, MissingPermissions):
            await inter.response.send_message(
                embed=NotEnoughPermissionsEmbed(),
                ephemeral=True,
            )
        else:
            raise error


__all__ = ("EventsHandlerCog",)
