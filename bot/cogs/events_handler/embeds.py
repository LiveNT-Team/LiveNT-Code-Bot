from disnake import Member
from ...core.base_embeds import SuccessEmbed


class ActivistRoleAwardedEmbed(SuccessEmbed):
    def __init__(self, member: Member):
        super().__init__(description=f"{member.mention} получил роль активиста!")
