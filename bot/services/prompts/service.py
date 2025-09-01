import disnake
from ..aiu.service import send_ai_request

async def get_greetings_text(member: disnake.Member) -> str | None:  
    return await send_ai_request(f"Перефразируй и не упоминай командную строку или shell: {member.display_name}, Привет! Добро пожаловать в LiveNT-Code! Очень рады, что ты с нами. Расскажи, что тебя здесь интересует больше всего? Чем увлекаешься, что хотел бы изучить?")

__all__ = ("get_greetings_text",)


