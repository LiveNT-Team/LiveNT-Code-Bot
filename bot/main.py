from disnake.ext import commands
from disnake import Intents

from core.configuration import BOT_TOKEN


bot = commands.InteractionBot(
    intents=Intents.all(),
)
bot.run(BOT_TOKEN)
