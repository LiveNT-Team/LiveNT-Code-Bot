from disnake.ext.commands import InteractionBot, MissingPermissions, CommandError
from disnake import Intents, AppCmdInter

from bot.core.configuration import BOT_TOKEN, TEST_GUILDS
from bot.core.logger import logger
from bot.cogs.help import HelpCog
from bot.cogs.personalities import PersonalitiesCog
from bot.cogs.settings import SettingsCog
from bot.cogs.stats import StatsCog

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
    }
]


@bot.event
async def on_ready() -> None:
    logger.info("Bot ready")


@bot.event
async def on_slash_command_error(inter: AppCmdInter, error: CommandError) -> None:
    if isinstance(error, MissingPermissions):
        await inter.response.send_message("You don't have permissions to execute this command")
    else:
        raise error


bot.run(BOT_TOKEN)
