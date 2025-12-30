from disnake.ext.commands import InteractionBot, CommandSyncFlags
from disnake import Intents

from core.configuration import BOT_TOKEN

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
[bot.add_cog(cog) for cog in {}]


bot.run(BOT_TOKEN)
