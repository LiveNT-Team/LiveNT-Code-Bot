import requests
import json
import base64
from pathlib import Path
from typing import Optional, Any
import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

PERSONALITIES: dict[str, dict[str, Any]] = {
    "assistant": {"name": "Ассистент", "description": "Будь лаконичным и полезным. Только суть.", "temperature": 0.7, "max_tokens": 1000},
    "warm": {"name": "Теплый помощник", "description": "Отвечай тепло и с пониманием. Кратко, но с заботой.", "temperature": 0.8, "max_tokens": 1200},
    "ideas": {"name": "Генератор идей", "description": "Думай нестандартно. Предлагай яркие и свежие идеи.", "temperature": 0.9, "max_tokens": 1500},
    "consultant": {"name": "Консультант", "description": "Будь точным. Отвечай как эксперт, без воды.", "temperature": 0.3, "max_tokens": 800},
    "programmer": {"name": "Программист", "description": "Отвечай как опытный разработчик. Четко, по делу, с примерами.", "temperature": 0.4, "max_tokens": 1200},
    "explorer": {"name": "Исследователь", "description": "Исследуй тему глубоко. Задавай уточняющие вопросы. Отвечай с интересом и стремлением к пониманию.", "temperature": 0.7, "max_tokens": 1500},
}


def send_ai_request(text: str, personality_name: str = "assistant", image_path: Optional[str] = None) -> Optional[str]:
    personality = PERSONALITIES[personality_name]
    messages = [{"role": "system", "content": personality["description"]}, {"role": "user", "content": text}]

    if image_path and Path(image_path).exists():
        if Path(image_path).stat().st_size <= 10 * 1024 * 1024:
            with open(image_path, "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
            ext = Path(image_path).suffix.lower()
            mime = {"png": "image/png", "gif": "image/gif", "webp": "image/webp", "bmp": "image/bmp"}.get(ext[1:], "image/jpeg")
            messages[1]["images"] = [{"base64": f"data:{mime};base64,{data}"}]

    data = {"custom_key": API_KEY, "messages": messages, "temperature": personality.get("temperature", 0.7), "max_tokens": personality.get("max_tokens", 1000)}

    response = requests.post(API_URL, headers={"Content-Type": "application/json"}, json=data, timeout=60)
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    return None


__all__ = ("send_ai_request",)
