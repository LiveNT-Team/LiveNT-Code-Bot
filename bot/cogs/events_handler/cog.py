from disnake.ext.commands import Cog, MissingPermissions
from disnake import AppCmdInter

from core.logger import logger
from core.embeds import NotEnoughPermissionsEmbed


class EventsHandlerCog(Cog):
    @Cog.listener()
    async def on_ready(self) -> None:
        logger.info("Bot is ready")

    @Cog.listener()
    async def on_slash_command_error(self, inter: AppCmdInter, error: Exception):
        if isinstance(error, MissingPermissions):
            await inter.response.send_message(
                embed=NotEnoughPermissionsEmbed(),
                ephemeral=True,
            )
        else:
            raise error


__all__ = ("EventsHandlerCog",)
