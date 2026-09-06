import logging
from groq import AsyncGroq, GroqError
from app.config import settings

logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self) -> None:
        self.client = AsyncGroq(api_key=settings.groq_api_key)

    async def generate_summary(self, prompt: str) -> str | None:
        try:
            response = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Ayno Assistant. Provide concise, helpful updates."},
                    {"role": "user", "content": prompt}
                ],
                model=settings.groq_model,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except GroqError as e:
            logger.error(f"Groq API Error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected Groq client failure: {e}")
            return None

    async def check_health(self) -> bool:
        try:
            return bool(settings.groq_api_key)
        except Exception:
            return False
