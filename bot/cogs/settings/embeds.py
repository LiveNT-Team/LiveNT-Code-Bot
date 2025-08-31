from disnake import TextChannel

from ...core.base_embeds import SuccessEmbed, ErrorEmbed, InfoEmbed


class AIEnabledEmbed(SuccessEmbed):
    def __init__(self) -> None:
        super().__init__(description="ИИ функционал включен")


class AIDisabledEmbed(SuccessEmbed):
    def __init__(self) -> None:
        super().__init__(description="ИИ функционал выключен")


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


class SettingsEmbed(InfoEmbed):
    def __init__(
        self,
        greetings_channel_id: int,
        ai_channel_id: int,
        is_ai_enabled: bool,
        is_greetings_enabled: bool,
    ) -> None:
        super().__init__(description="Настройки бота:")
        self.add_field(name="Канал для приветствий", value=f"<#{greetings_channel_id}>", inline=False)
        self.add_field(name="Канал для ИИ", value=f"<#{ai_channel_id}>", inline=False)
        self.add_field(name="Приветствия", value="Включен" if is_greetings_enabled else "Выключен", inline=False)
        self.add_field(name="ИИ функционал", value="Включен" if is_ai_enabled else "Выключен", inline=False)
