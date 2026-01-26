from disnake import AppCmdInter
from disnake.ext.commands import Cog, slash_command
from bot.core.base_embeds import InfoEmbed
from bot.cogs.help.views import HelpView


class HelpCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="help", description="Помощь")
    async def help_command(self, inter: AppCmdInter):
        await inter.response.send_message(
            embed=InfoEmbed(
                description="Выберите раздел, по которому вы хотите получить помощь"
            ),
            view=HelpView(),
            ephemeral=True,
        )


def setup(bot):
    bot.add_cog(HelpCog(bot))
