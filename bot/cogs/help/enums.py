from enum import Enum


class HelpMenuSectionsEnum(Enum):
    ADMINISTRATORS = (
        "Администрирование",
        "Управление ролями администраторов и модераторов",
        (
            ("/set_admin_role", "Установить роль администратора"),
            ("/set_main_admin_role", "Установить роль главного администратора"),
            ("/set_major_admin_role", "Установить роль старшего администратора"),
            ("/set_minor_admin_role", "Установить роль младшего администратора"),
            ("/set_moder_role", "Установить роль модератора"),
            ("/set_main_moder_role", "Установить роль главного модератора"),
            ("/set_major_moder_role", "Установить роль старшего модератора"),
            ("/set_minor_moder_role", "Установить роль младшего модератора"),
        ),
    )
    GREETINGS = (
        "Приветствия",
        "Система приветствия новых участников",
        (
            ("/enable_greetings", "Включить приветствия"),
            ("/disable_greetings", "Выключить приветствия"),
            ("/set_greetings_channel", "Установить канал для приветствий"),
        ),
    )
    PERSONALITIES = (
        "Личности ИИ",
        "Управление личностями ИИ ассистента",
        (
            ("/get_ai_personality", "Показать текущую личность ИИ"),
            ("/set_ai_personality", "Установить новую личность"),
            ("/get_personalities", "Показать список всех личностей"),
        ),
    )
    SETTINGS = (
        "Настройки",
        "Управление настройками сервера",
        (
            ("/get_settings", "Показать все настройки сервера"),
            ("/set_developer_role", "Установить роль разработчика"),
            ("/set_activist_enabled", "Включить/выключить систему активиста"),
            ("/set_activist_role", "Установить роль активиста"),
            ("/set_activist_messages", "Установить количество сообщений для активиста"),
        ),
    )
    AI_CHAT = (
        "ИИ Чат",
        "Система чата с ИИ",
        (
            ("/enable_ai_chat", "Включить чат с ИИ"),
            ("/disable_ai_chat", "Выключить чат с ИИ"),
            ("/set_ai_channel", "Установить канал для ИИ"),
        ),
    )
    STATISTICS = (
        "Статистика",
        "Просмотр статистики",
        (("/stats", "Показать статистику сообщений участника"),),
    )

    def __init__(self, label: str, description: str, commands: tuple):
        self.label = label
        self.description = description
        self.commands = commands
