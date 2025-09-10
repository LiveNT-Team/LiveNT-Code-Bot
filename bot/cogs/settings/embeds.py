from disnake import Role, TextChannel

from ...core.base_embeds import SuccessEmbed, ErrorEmbed, InfoEmbed


class AIEnabledEmbed(SuccessEmbed):
    def __init__(self) -> None:
        super().__init__(description="ИИ функционал включен")


class AIDisabledEmbed(SuccessEmbed):
    def __init__(self) -> None:
        super().__init__(description="ИИ функционал выключен")


class ActivistExtraditingEnabledEmbed(SuccessEmbed):
    def __init__(self) -> None:
        super().__init__(description="Выдача активиста включена")


class ActivistExtraditingDisabledEmbed(SuccessEmbed):
    def __init__(self) -> None:
        super().__init__(description="Выдача активиста отключена")


class ActivistRoleSetEmbed(SuccessEmbed):
    def __init__(self) -> None:
        super().__init__(description="Роль активиста установлена")


class ActivistMessagesCountSetEmbed(SuccessEmbed):
    def __init__(self) -> None:
        super().__init__(description="Количество сообщений для получения активиста установлено")


class ActivistMessagesCountCantBeLessThanZeroEmbed(SuccessEmbed):
    def __init__(self) -> None:
        super().__init__(description="Количество сообщений для получения активиста не может быть меньше единицы")


class AIChannelSetEmbed(SuccessEmbed):
    def __init__(self, channel: TextChannel) -> None:
        super().__init__(description=f"Установлен новый канал для общения с ИИ: {channel.mention}")


class GreetingsEnabledEmbed(SuccessEmbed):
    def __init__(self) -> None:
        super().__init__(description="Приветствия включены")


class GreetingsDisabledEmbed(SuccessEmbed):
    def __init__(self) -> None:
        super().__init__(description="Приветствия выключены")


class GreetingsChannelSetEmbed(SuccessEmbed):
    def __init__(self, channel: TextChannel) -> None:
        super().__init__(description=f"Установлен новый канал для приветствий: {channel.mention}")


class DeveloperRoleSetEmbed(SuccessEmbed):
    def __init__(self, role: Role) -> None:
        super().__init__(description=f"Установлена роль для разработчиков сервера: {role.mention}")


class SettingsEmbed(InfoEmbed):
    def __init__(
        self,
        greetings_channel_id: int,
        ai_channel_id: int,
        activist_role_id: int,
        activist_role_messages_count: int,
        is_ai_enabled: bool,
        is_greetings_enabled: bool,
        is_activist_role_extraditing: bool,
        developer_role_id: int,
    ) -> None:
        super().__init__(description="Настройки бота:")
        self.add_field(name="Канал для приветствий", value=f"<#{greetings_channel_id}>", inline=False)
        self.add_field(name="Роль активиста", value=f"<@&{activist_role_id}>", inline=False)
        self.add_field(name="Роль разработчика", value=f"<@&{developer_role_id}>", inline=False)
        self.add_field(name="Количество сообщений для получения активиста", value=activist_role_messages_count, inline=False)
        self.add_field(name="Канал для ИИ", value=f"<#{ai_channel_id}>", inline=False)
        self.add_field(name="Приветствия", value="Включен" if is_greetings_enabled else "Выключен", inline=False)
        self.add_field(name="ИИ функционал", value="Включен" if is_ai_enabled else "Выключен", inline=False)
        self.add_field(name="Выдача активиста", value="Включен" if is_activist_role_extraditing else "Выключен", inline=False)
