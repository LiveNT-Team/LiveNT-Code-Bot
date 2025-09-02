from disnake.ext.commands import InteractionBot, CommandSyncFlags
from disnake import Intents

from bot.core.configuration import BOT_TOKEN, TEST_GUILDS
from bot.cogs.help import HelpCog
from bot.cogs.personalities import PersonalitiesCog
from bot.cogs.settings import SettingsCog
from bot.cogs.stats import StatsCog
from bot.cogs.events_handler import EventsHandlerCog
from bot.cogs.ai import AICog

bot = InteractionBot(
    intents=Intents(
        messages=True,
        guilds=True,
        members=True,
    ),
    test_guilds=TEST_GUILDS,
    command_sync_flags=CommandSyncFlags(
        sync_commands_debug=True,
    ),
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
