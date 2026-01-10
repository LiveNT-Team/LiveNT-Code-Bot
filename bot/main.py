from disnake.ext.commands import InteractionBot, CommandSyncFlags, MissingPermissions
from disnake import Intents, AppCmdInter

from services.mysqliup import MySqliUp
from services.guilds_settings import init_guild_settings

from core.configuration import BOT_TOKEN
from core.embeds import NotEnoughPermissionsEmbed
from cogs.settings.cog import SettingsCog
from cogs.personalities.cog import PersonalitiesCog
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

async def setup_database():
    try:
        db = MySqliUp()
        await db.connect()
        await init_guild_settings(db)
    except Exception as error:
        raise error

@bot.event
async def on_ready() -> None:
    logger.info("Bot is ready")
	await setup_database()


@bot.event
async def on_slash_command_error(inter: AppCmdInter, error: Exception):
    if isinstance(error, MissingPermissions):
        await inter.response.send_message(
            embed=NotEnoughPermissionsEmbed(),
            ephemeral=True,
        )
    else:
        raise error


[bot.add_cog(cog) for cog in {SettingsCog(), PersonalitiesCog()}]


bot.run(BOT_TOKEN)




