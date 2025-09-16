import httpx
import base64
from pathlib import Path

from ...core.configuration import PERSONALITIES, AI_API_KEY, AI_API_URL, DEFAULT_PERSONALITY_NAME
from ...core.typed_dicts import Personality


async def send_ai_request(
    text: str,
    personality: Personality = PERSONALITIES[DEFAULT_PERSONALITY_NAME],
    image_path: str | None = None,
) -> str | None:
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

    if image_path and (image_path.startswith("http://") or image_path.startswith("https://")):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(image_path, timeout=30)
                if response.status_code == 200 and len(response.content) <= 10 * 1024 * 1024:
                    data = base64.b64encode(response.content).decode("utf-8")
                    ext = image_path.split(".")[-1].lower().split("?")[0] 
                    mime = {"png": "image/png", "webp": "image/webp"}.get(
                        ext,
                        "image/jpeg",
                    )
                    messages[1]["images"] = [
                        {
                            "base64": f"data:{mime};base64,{data}",
                        },
                    ]
        except (httpx.RequestError, httpx.TimeoutException):
            pass
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
