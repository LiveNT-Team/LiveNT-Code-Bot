from ...core.base_embeds import SuccessEmbed, ErrorEmbed, InfoEmbed
from ...core.configuration import PersonalitiesEnum, PERSONALITIES


class PersonalitySetEmbed(SuccessEmbed):
    def __init__(self, personality_name: PersonalitiesEnum) -> None:
        super().__init__(description=f"Вы изменили личность ИИ модели на: `{personality_name}`.")


class PersonalitiesListEmbed(InfoEmbed):
    def __init__(
        self,
        current_personality_name: PersonalitiesEnum,
        personalities: dict[PersonalitiesEnum, str] = PERSONALITIES,
    ) -> None:
        super().__init__(description=f"Список доступных личностей:")
        for [personality_name, personality_desc] in personalities.items():
            if personality_name == current_personality_name:
                self.add_field(f"{personality_name} (выбрано)", personality_desc)
            else:
                self.add_field(personality_name, personality_desc)
