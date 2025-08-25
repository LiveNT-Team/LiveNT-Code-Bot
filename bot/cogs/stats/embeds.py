from disnake import Member
from ...core.base_embeds import InfoEmbed


class MemberStatsEmbed(InfoEmbed):
    def __init__(
        self,
        member: Member,
        messages_count: int,
    ) -> None:
        super().__init__(description=f"Статистика участника {member.mention}:")
        self.add_field("Сообщений отправлено", messages_count, inline=False)
