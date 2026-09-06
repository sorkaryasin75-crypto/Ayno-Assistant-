import logging
import httpx
from app.config import settings

logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self) -> None:
        self.bot_token = settings.telegram_bot_token
        self.chat_id = settings.telegram_chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    async def send_message(self, text: str) -> bool:
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(url, json=payload)
                if response.status_code == 429:
                    retry_after = response.json().get("parameters", {}).get("retry_after", 5)
                    logger.warning(f"Telegram Rate limit hit. Retry after {retry_after}s")
                    return False
                
                response.raise_for_status()
                data = response.json()
                return data.get("ok", False)
            except httpx.HTTPStatusError as e:
                logger.error(f"Telegram HTTP Error {e.response.status_code}: {e.response.text}")
                return False
            except httpx.RequestError as e:
                logger.error(f"Telegram Connection Error: {e}")
                return False

    async def check_health(self) -> bool:
        url = f"{self.base_url}/getMe"
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(url)
                return response.status_code == 200 and response.json().get("ok", False)
            except Exception:
                return False
