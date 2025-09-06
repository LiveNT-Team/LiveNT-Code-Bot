from ...core.base_embeds import InfoEmbed
from .enums import HelpMenuSectionsEnum


class HelpForSectionEmbed(InfoEmbed):
    def __init__(self, section_name: HelpMenuSectionsEnum):
        super().__init__()
        match section_name:
            case HelpMenuSectionsEnum.AI:
                self.add_field("ИИ Функционал", 
                    "/enable ai - включить ИИ функционал\n"
                    "/disable ai - отключить ИИ функционал\n"
                    "/ask text:запрос personality_name:название_личности - Запрос к ИИ также можно через @ без выбора личности")
            case HelpMenuSectionsEnum.SETTINGS:
                self.add_field("Настройка сервера", 
                    "/settings - Вывести информацию настроек сервера\n"
                    "/set ai_channel channel:#канал - Установить канал для общения с ИИ\n"
                    "/set greetings_channel channel:#канал - Установить канал для приветствия от ИИ при входе\n"
                    "/disable greetings - отключить приветствие от ИИ при входе\n"
                    "/enable greetings - включить приветствие от ИИ при входе")
            case HelpMenuSectionsEnum.PERSONALITIES:
                self.add_field("Личности ИИ", 
                    "/change personality personality_name:название_личности - Выбрать личность ИИ\n"
                    "/get personalities - Список личностей ИИ")
            case HelpMenuSectionsEnum.STATS:
                self.add_field("Статистика", 
                    "/stats member:@Участник - Статистика ввода сообщений\n"
                    "/enable extraditing_activist - Включить выдачу роли Активист\n"
                    "/disable extraditing_activist - Отключить выдачу роли Активист\n"
                    "/set activist_messages_count count:число - Установить порог для получения роли Активист\n"
                    "/set activist_role role:@роль - Установить роль Активист")


class HelpEmbed(InfoEmbed):
    def __init__(self) -> None:
        super().__init__(description="Выберите раздел, по которому вы хотите получить помощь.")
