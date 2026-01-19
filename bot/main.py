from disnake.ext.commands import InteractionBot, CommandSyncFlags, MissingPermissions
from disnake import Intents, AppCmdInter

from core.configuration import BOT_TOKEN
from core.embeds import NotEnoughPermissionsEmbed
from cogs.settings.cog import SettingsCog
from cogs.personalities.cog import PersonalitiesCog
from cogs.administrators.cog import AdministratorsCog
from cogs.events_handler.cog import EventsHandlerCog
from core.logger import logger

bot = InteractionBot(
    intents=Intents(
        messages=True,
        guilds=True,
        members=True,
        message_content=True,
    ),
    command_sync_flags=CommandSyncFlags(
        sync_commands_debug=True,
    ),
)


@bot.event
async def on_ready() -> None:
    logger.info("Bot is ready")


@bot.event
async def on_slash_command_error(inter: AppCmdInter, error: Exception):
    if isinstance(error, MissingPermissions):
        await inter.response.send_message(
            embed=NotEnoughPermissionsEmbed(),
            ephemeral=True,
        )
    else:
        raise error


[
    bot.add_cog(cog)
    for cog in {
        SettingsCog(),
        PersonalitiesCog(),
        EventsHandlerCog(bot),
        AdministratorsCog(),
    }
]


bot.run(BOT_TOKEN)
