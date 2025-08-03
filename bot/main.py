from disnake.ext import commands
from disnake import Intents

from core.configuration import BOT_TOKEN, TEST_GUILDS
from core.logger import logger

bot = commands.InteractionBot(
    intents=Intents(message_content=True),
    test_guilds=TEST_GUILDS,
    sync_commands_debug=True,
)


@bot.event
async def on_ready() -> None:
    logger.info("Bot ready")


bot.run(BOT_TOKEN)
