import httpx
import base64
from pathlib import Path

from ...core.configuration import PERSONALITIES, AI_API_KEY, AI_API_URL


async def send_ai_request(
    text: str,
    personality_name: str = "assistant",
    image_path: str | None = None,
) -> str | None:
    personality = PERSONALITIES[personality_name]
    messages = [
        {
            "role": "system",
            "content": personality["description"],
        },
        {
            "role": "user",
            "content": text,
        },
    ]

    if image_path and Path(image_path).exists():
        if Path(image_path).stat().st_size <= 10 * 1024 * 1024:
            with open(image_path, "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
            ext = Path(image_path).suffix.lower()
            mime = {"png": "image/png", "gif": "image/gif", "webp": "image/webp", "bmp": "image/bmp"}.get(
                ext[1:],
                "image/jpeg",
            )
            messages[1]["images"] = [
                {
                    "base64": f"data:{mime};base64,{data}",
                },
            ]
    async with httpx.AsyncClient() as httpx_client:
        response = await httpx_client.post(
            AI_API_URL,
            headers={"Content-Type": "application/json"},
            json={
                "custom_key": AI_API_KEY,
                "messages": messages,
                "temperature": personality["temperature"],
                "max_tokens": personality["max_tokens"],
            },
            timeout=60,
        )
    match response.status_code:
        case 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        case _:
            return None


__all__ = ("send_ai_request",)
