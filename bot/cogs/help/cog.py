from disnake import AppCmdInter
from disnake.ext import commands

from .embeds import HelpEmbed
from .views import HelpView


class HelpCog(commands.Cog):
    @commands.slash_command(name="help", description="Помощь")
    async def help(self, inter: AppCmdInter) -> None:
        await inter.response.send_message(
            embed=HelpEmbed(),
            view=HelpView(),
            ephemeral=True,
        )


__all__ = ("HelpCog",)
