from ...core.base_embeds import ErrorEmbed


class AIErrorEmbed(ErrorEmbed):
    def __init__(self) -> None:
        super().__init__(description="Произошла ошибка при обработке вашего запроса.")
