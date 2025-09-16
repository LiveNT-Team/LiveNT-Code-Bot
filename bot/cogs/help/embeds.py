from ...core.base_embeds import InfoEmbed
from .enums import HelpMenuSectionsEnum


class HelpForSectionEmbed(InfoEmbed):
    def __init__(self, section_name: HelpMenuSectionsEnum):
        super().__init__()
        match section_name:
            case HelpMenuSectionsEnum.AI:
                self.add_field(
                    "ИИ Функционал",
                    "</enable ai:0> - включить ИИ функционал\n"
                    "</disable ai:0> - отключить ИИ функционал\n"
                    "</ask:0> - Запрос к ИИ также можно через @ без выбора личности")
            case HelpMenuSectionsEnum.SETTINGS:
                self.add_field(
                    "Настройка сервера",
                    "</settings:0> - Вывести информацию настроек сервера\n"
                    "</set:0> - Установить канал для общения с ИИ\n"
                    "</set:0> - Установить канал для приветствия от ИИ при входе\n"
                    "</disable greetings:0> - отключить приветствие от ИИ при входе\n"
                    "</enable greetings:0> - включить приветствие от ИИ при входе",
                )
            case HelpMenuSectionsEnum.PERSONALITIES:
                self.add_field("Личности ИИ", 
                    "</change personality:0> - Выбрать личность ИИ\n"
                    "</get personalities:0> - Список личностей ИИ")
            case HelpMenuSectionsEnum.STATS:
                self.add_field("Статистика", 
                    "</stats:0> - Статистика ввода сообщений\n"
                    "</enable extraditing_activist:0> - Включить выдачу роли Активист\n"
                    "</disable extraditing_activist:0> - Отключить выдачу роли Активист\n"
                    "</set activist_messages_count:0> - Установить порог для получения роли Активист\n"
                    "</set activist_role:0> - Установить роль Активист")


class HelpEmbed(InfoEmbed):
    def __init__(self) -> None:
        super().__init__(description="Выберите раздел, по которому вы хотите получить помощь.")
