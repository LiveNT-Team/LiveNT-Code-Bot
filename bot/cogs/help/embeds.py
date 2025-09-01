from ...core.base_embeds import InfoEmbed
from .enums import HelpMenuSectionsEnum


class HelpForSectionEmbed(InfoEmbed):
    def __init__(self, section_name: HelpMenuSectionsEnum):
        super().__init__()
        match section_name:
            case HelpMenuSectionsEnum.AI:
                ...
            case HelpMenuSectionsEnum.SETTINGS:
                ...
            case HelpMenuSectionsEnum.PERSONALITIES:
                ...
            case HelpMenuSectionsEnum.STATS:
                ...


class HelpEmbed(InfoEmbed):
    def __init__(self) -> None:
        super().__init__(description="Выберите раздел, по которому вы хотите получить помощь.")
