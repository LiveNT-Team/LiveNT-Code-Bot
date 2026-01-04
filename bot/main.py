from disnake.ext.commands import InteractionBot, CommandSyncFlags
from disnake import Intents
from logging import getLogger

from core.configuration import BOT_TOKEN
from cogs.settings.cog import SettingsCog
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
    logger.info("Bot ready")


[bot.add_cog(cog) for cog in {SettingsCog()}]


bot.run(BOT_TOKEN)
