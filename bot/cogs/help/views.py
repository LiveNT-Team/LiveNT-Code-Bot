from disnake import MessageInteraction, SelectOption
from disnake.ui import Select, View, select
from .enums import HelpMenuSectionsEnum
from .embeds import HelpForSectionEmbed


class HelpView(View):
    def __init__(self):
        super().__init__(timeout=120)

    @select(
        placeholder="Выберите раздел помощи",
        min_values=1,
        max_values=1,
        options=[
            SelectOption(
                label=section.label,
                description=section.description,
                value=section.name,
            )
            for section in HelpMenuSectionsEnum
        ],
    )
    async def help_menu_select(self, select: Select, inter: MessageInteraction):
        section = HelpMenuSectionsEnum[select.values[0]]
        await inter.response.send_message(
            embed=HelpForSectionEmbed(section),
            ephemeral=True,
        )
