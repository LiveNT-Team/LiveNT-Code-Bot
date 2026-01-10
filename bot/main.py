import asyncio
from disnake.ext.commands import InteractionBot, CommandSyncFlags
from disnake import Intents

from core.configuration import BOT_TOKEN
from services.mysqliup import MySqliUp
from services.guilds_settings import init_guild_settings
from core.logger import logger


async def setup_database():
    """Инициализировать базу данных и сервис guild_settings"""
    try:
        db = MySqliUp()
        await db.connect()
        await init_guild_settings(db)
        logger.info("Database and guild_settings service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


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
async def on_ready():
    """Событие готовности бота"""
    logger.info(f"Bot logged in as {bot.user}")
    await setup_database()


# Загружаем коги вручную
async def load_cogs():
    """Загрузить все коги"""
    from cogs.settings.cog import SettingsCog
    from cogs.events_handler.cog import EventsHandlerCog
    from cogs.ai.cog import AICog
    from cogs.stats.cog import StatsCog

    bot.add_cog(SettingsCog())
    bot.add_cog(EventsHandlerCog(bot))
    bot.add_cog(AICog(bot))
    bot.add_cog(StatsCog(bot))
    logger.info("Cogs loaded successfully")


@bot.event
async def on_connect():
    """Загрузить коги при подключении"""
    await load_cogs()


bot.run(BOT_TOKEN)
