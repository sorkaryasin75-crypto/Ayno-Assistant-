import asyncio
import logging
import os
import random
from groq import Groq
from telegram import Bot
from telegram.error import TelegramError

# --- Logging Config ---
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("AynoAssistant")

# --- Environment Variables ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")

# সিকিউরিটি ফিল্টার ও ভ্যালিডেশন
if not all([GROQ_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_GROUP_ID]):
    logger.critical(
        "❌ Environment Variables missing! Check GROQ_API_KEY, TELEGRAM_BOT_TOKEN, and TELEGRAM_GROUP_ID"
    )
    exit(1)

# ক্লায়েন্ট ইনিশিয়ালাইজেশন
groq_client = Groq(api_key=GROQ_API_KEY)
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

TIPS_PROMPTS = [
    "Write a short, practical Telegram tip in Bengali about privacy, active sessions, and 2-step verification.",
    "Share a useful Telegram feature tip in Bengali like Chat Folders, Saved Messages, or Custom Themes.",
    "Give a quick tip in Bengali for Telegram group/channel admins regarding auto-delete, admin rights, or slow mode.",
    "Write a hidden Telegram shortcut, bot trick, or power-user tip in Bengali.",
]


def generate_telegram_tip() -> str:
    """Groq API থেকে নিরাপদভাবে Telegram Tip তৈরি করে"""
    selected_prompt = random.choice(TIPS_PROMPTS)

    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are 'Ayno Assistant', a friendly Telegram tips AI. "
                        "Write a short, highly useful Telegram tip in Bengali using emojis. "
                        "Keep it strictly within 2-3 sentences. "
                        "Do NOT use raw Markdown symbols like asterisks or hashtags. Return plain clean text."
                    ),
                },
                {"role": "user", "content": selected_prompt},
            ],
            temperature=0.7,
            max_tokens=200,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"❌ Groq API Error: {e}")
        return None


async def send_tip_job():
    """মেসেজ ফরম্যাট করে নিরাপদে Telegram-এ পাঠায়"""
    tip_text = generate_telegram_tip()

    if not tip_text:
        logger.warning("⚠️ No tip generated. Retrying in next cycle.")
        return

    # HTML Formatting (Markdown এরর এড়াতে এটি ১০০% নিরাপদ)
    formatted_message = f"<b>🤖 Ayno Assistant - Telegram Tip</b>\n\n{tip_text}"

    try:
        await telegram_bot.send_message(
            chat_id=TELEGRAM_GROUP_ID, text=formatted_message, parse_mode="HTML"
        )
        logger.info("✅ Tip successfully sent to Telegram Group!")
    except TelegramError as e:
        logger.error(f"❌ Telegram Delivery Error: {e}")


async def main():
    logger.info(
        "🚀 Ayno Assistant started. Posting tips every 5 minutes..."
    )

    while True:
        await send_tip_job()
        await asyncio.sleep(300)  # ৩০০ সেকেন্ড = ৫ মিনিট


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Ayno Assistant stopped.")
