from .base_embeds import ErrorEmbed


class TheCommandDoesNotSupportDMEmbed(ErrorEmbed):
    def __init__(self) -> None:
        super().__init__(description="Эта команда не поддерживает использование с личных сообщениях.")


class YouCannotMentionBotInsteadMemberEmbed(ErrorEmbed):
    def __init__(self) -> None:
        super().__init__(description="Вы не можете передать бота вместо участника в параметр.")
