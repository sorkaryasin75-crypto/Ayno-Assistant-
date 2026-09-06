import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.groq_client import GroqService
from app.core.telegram_client import TelegramService

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()
groq_service = GroqService()
telegram_service = TelegramService()

async def automated_task() -> None:
    logger.info("Executing 5-minute automated pipeline...")
    prompt = "Generate a short, motivating periodic check-in message for today."
    
    ai_response = await groq_service.generate_summary(prompt)
    if ai_response:
        success = await telegram_service.send_message(f"<b>Ayno Assistant Auto Update</b>\n\n{ai_response}")
        if success:
            logger.info("Automated notification dispatched successfully.")
        else:
            logger.error("Failed to send Telegram message.")
    else:
        logger.error("Groq AI response generation failed during automated task.")

def setup_scheduler() -> AsyncIOScheduler:
    scheduler.add_job(automated_task, "interval", minutes=5, id="ayno_5min_job", replace_existing=True)
    return scheduler
