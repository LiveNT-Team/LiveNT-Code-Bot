from core.base_embeds import InfoEmbed
from .enums import HelpMenuSectionsEnum


class HelpForSectionEmbed(InfoEmbed):
    def __init__(self, section: HelpMenuSectionsEnum):
        commands_text = "\n".join(f"`{cmd}` — {desc}" for cmd, desc in section.commands)
        super().__init__(description=f"**{section.label}**\n\n{commands_text}")
