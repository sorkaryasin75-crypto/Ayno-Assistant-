import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from telegram import Bot
from telegram.error import TelegramError
from groq import Groq

# --- কনফিগারেশন ---
BOT_TOKEN = "8680178701:AAEdRETzMseHbOZuMmQFXpR9RemM-CQ8dl0"  # বটের টোকেন
CHAT_ID = "-1002352180501"                  # গ্রুপের Chat ID (মাইনাস সহ)
GROQ_API_KEY = "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"      # Groq API Key

# ইনিশিয়ালাইজেশন
bot = Bot(token=BOT_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)

# Groq API দিয়ে Telegram Tips জেনারেট করার ফাংশন
def generate_telegram_tip():
    prompt = (
        "Generate a short, extremely helpful Telegram tip or feature secret for users. "
        "Keep it concise, engaging, under 250 characters, and use appropriate emojis. "
        "Write in simple English or Bangla suitable for a Telegram community."
    )
    
    response = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a Telegram power-user expert providing daily short tips."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-8b-8192",  # সঠিক ও সক্রিয় মডেল
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

# অটোমেটিক AI মেসেজ পাঠানোর ব্যাকগ্রাউন্ড টাস্ক
async def auto_send_ai_tips():
    while True:
        try:
            tip_content = generate_telegram_tip()
            full_message = f"💡 **Telegram Tip of the Day** 💡\n\n{tip_content}"
            
            await bot.send_message(chat_id=CHAT_ID, text=full_message, parse_mode="Markdown")
            print("[SUCCESS] Groq AI থেকে টিপস তৈরি করে গ্রুপে পাঠানো হয়েছে।")
            
        except TelegramError as e:
            print(f"[ERROR] Telegram সমস্যা: {e}")
        except Exception as e:
            print(f"[ERROR] Groq API সমস্যা: {e}")
            
        await asyncio.sleep(3600)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(auto_send_ai_tips())
    yield
    task.cancel()

app = FastAPI(title="Groq AI Telegram Tips Bot", lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "running", "bot": "Groq AI Auto Tips Bot is active"}
