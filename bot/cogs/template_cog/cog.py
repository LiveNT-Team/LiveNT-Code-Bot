from disnake.ext.commands import Cog, Param, slash_command
from disnake import AppCmdInter


class TemplateCog(Cog):
    @slash_command()
    async def template(self, inter: AppCmdInter) -> None:
        pass


__all__ = ("TemplateCog",)
