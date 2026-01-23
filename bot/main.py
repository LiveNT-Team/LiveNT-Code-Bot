from disnake.ext.commands import InteractionBot, CommandSyncFlags
from disnake import Intents

from core.configuration import BOT_TOKEN
from cogs.settings.cog import SettingsCog
from cogs.personalities.cog import PersonalitiesCog
from cogs.administrators.cog import AdministratorsCog
from cogs.events_handler.cog import EventsHandlerCog
from cogs.greetings.cog import GreetingsCog
from cogs.ai_chat.cog import AIChat
from cogs.bans.cog import BansCog
from cogs.muts.cog import MutsCog

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


[
    bot.add_cog(cog)
    for cog in {
        SettingsCog(),
        PersonalitiesCog(),
        EventsHandlerCog(),
        AdministratorsCog(),
        GreetingsCog(),
        AIChat(bot=bot),
        BansCog(),
        MutsCog(),
    }
]


bot.run(BOT_TOKEN)
