from disnake.ext.commands import InteractionBot, MissingPermissions, CommandError
from disnake import Intents, AppCmdInter

from bot.core.configuration import BOT_TOKEN, TEST_GUILDS
from bot.core.logger import logger
from bot.cogs.help import HelpCog
from bot.cogs.personalities import PersonalitiesCog
from bot.cogs.settings import SettingsCog
from bot.cogs.stats import StatsCog
from bot.cogs.events_handler import EventsHandlerCog
from bot.cogs.ai import AICog

bot = InteractionBot(
    intents=Intents(messages=True),
    test_guilds=TEST_GUILDS,
    sync_commands_debug=True,
)
[
    bot.add_cog(cog)
    for cog in {
        HelpCog(),
        PersonalitiesCog(),
        SettingsCog(),
        StatsCog(),
        EventsHandlerCog(bot=bot),
        AICog(),
    }
]


bot.run(BOT_TOKEN)
