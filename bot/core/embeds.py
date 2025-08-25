from .base_embeds import ErrorEmbed


class TheCommandDoesNotSupportDMEmbed(ErrorEmbed):
    def __init__(self) -> None:
        super().__init__(description="Эта команда не поддерживает использование с личных сообщениях.")
