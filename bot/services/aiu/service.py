import requests
import json
import base64
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
PERSONALITIES_FILE_PATH = BASE_DIR / "bot/core/personalities.json"


def load_personalities():
    try:
        with open(PERSONALITIES_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def send_ai_request(
    text: str,
    personality_name: str = "assistant",
    image_path: Optional[str] = None,
) -> Optional[str]:
    personalities = load_personalities()

    if personality_name not in personalities:
        return None

    personality = personalities[personality_name]
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
        try:
            if Path(image_path).stat().st_size <= 10 * 1024 * 1024:
                with open(image_path, "rb") as f:
                    data = base64.b64encode(f.read()).decode("utf-8")
                ext = Path(image_path).suffix.lower()
                mime = {"png": "image/png", "gif": "image/gif", "webp": "image/webp", "bmp": "image/bmp"}.get(ext[1:], "image/jpeg")
                messages[1]["images"] = [{"base64": f"data:{mime};base64,{data}"}]
        except:
            pass

    data = {
        "custom_key": API_KEY,
        "messages": messages,
        "temperature": personality.get("temperature", 0.7),
        "max_tokens": personality.get("max_tokens", 1000),
    }

    try:
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            json=data,
            timeout=60,
        )
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        return None
    except:
        return None
