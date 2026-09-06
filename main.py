import asyncio
import logging
import os
import random
from groq import Groq
from telegram import Bot
from telegram.error import TelegramError, NetworkError, RetryAfter

# --- প্রফেশনাল লগিং কনফিগারেশন ---
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("AynoAssistant")

# --- Environment Variables ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")

# ভ্যারিয়েবল চেকিং (ফেইল সেফ)
if not all([GROQ_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_GROUP_ID]):
    logger.critical(
        "❌ Environment Variables missing! Check GROQ_API_KEY, TELEGRAM_BOT_TOKEN, and TELEGRAM_GROUP_ID in Railway."
    )
    exit(1)

# ক্লায়েন্ট ইনিশিয়ালাইজেশন
groq_client = Groq(api_key=GROQ_API_KEY)
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)

TIPS_PROMPTS = [
    "Write a short, highly useful Telegram tip in Bengali about privacy, active sessions, or 2-step verification.",
    "Share a unique Telegram feature tip in Bengali like Chat Folders, Saved Messages, or Custom Themes.",
    "Give a quick Telegram tip in Bengali for group admins regarding auto-delete, admin rights, or slow mode.",
    "Write a hidden Telegram shortcut, bot trick, or power-user tip in Bengali.",
]


def generate_telegram_tip() -> str:
    """Groq API থেকে ১০০% নির্ভুলভাবে মেসেজ জেনারেট করার ফাংশন"""
    selected_prompt = random.choice(TIPS_PROMPTS)

    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ১০০% অ্যাক্টিভ ও নির্ভরযোগ্য মডেল
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are 'Ayno Assistant', an expert Telegram tips AI. "
                        "Provide a short, highly practical Telegram tip in clean Bengali with emojis. "
                        "Strictly keep it within 2 sentences. "
                        "Do NOT use markdown headers, bold tags, or asterisks (*). Return clean plain text."
                    ),
                },
                {"role": "user", "content": selected_prompt},
            ],
            temperature=0.7,
            max_tokens=150,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"❌ Groq API Error: {e}")
        return None


async def send_tip_job():
    """টেলিগ্রাম গ্রুপে মেসেজ পাঠানোর নিরাপদ ফাংশন"""
    tip_text = generate_telegram_tip()

    if not tip_text:
        logger.warning("⚠️ Message generation failed, skipping this cycle...")
        return

    # HTML ফরম্যাটিং (পার্স এরর রিমুভ করার জন্য)
    formatted_message = f"<b>🤖 Ayno Assistant - Telegram Tip</b>\n\n{tip_text}"

    try:
        await telegram_bot.send_message(
            chat_id=TELEGRAM_GROUP_ID,
            text=formatted_message,
            parse_mode="HTML",
        )
        logger.info("✅ Successfully sent message to Telegram group!")

    except RetryAfter as e:
        logger.warning(f"⚠️ Rate limited by Telegram. Waiting {e.retry_after} seconds...")
        await asyncio.sleep(e.retry_after)
    except NetworkError as e:
        logger.error(f"❌ Network issue encountered: {e}")
    except TelegramError as e:
        logger.error(f"❌ Telegram API Error: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected Error in send_job: {e}")


async def main():
    logger.info("🚀 Ayno Assistant 24/7 Engine Started! Posting every 5 minutes...")

    while True:
        try:
            await send_tip_job()
        except Exception as e:
            # ব্যাকগ্রাউন্ড কোনো আনহ্যান্ডেলড এরর আসলেও প্রোগ্রাম বন্ধ হবে না
            logger.error(f"⚠️ Exception in main loop, keeping system alive: {e}")

        # ৫ মিনিট (৩০০ সেকেন্ড) পাওয়ার সেভিং স্লিপ
        await asyncio.sleep(300)


if __name__ == "__main__":
    # অটো-রিস্টার্ট মেকানিজম (২৪/৭ নিরবচ্ছিন্ন সার্ভিস নিশ্চিত করে)
    while True:
        try:
            asyncio.run(main())
        except (KeyboardInterrupt, SystemExit):
            logger.info("🛑 Ayno Assistant manually stopped.")
            break
        except Exception as crash_error:
            logger.critical(f"⚠️ System crashed! Auto-restarting in 10 seconds... Error: {crash_error}")
            import time
            time.sleep(10)
