import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from telegram import Bot
from telegram.error import TelegramError
import google.generativeai as genai

# --- কনফিগারেশন ---
BOT_TOKEN = "8680178701:AAEdRETzMseHbOZuMmQFXpR9RemM-CQ8dl0"  # আপনার টেলিগ্রাম বটের টোকেন দিন
CHAT_ID = "-1002352180501"                  # আপনার গ্রুপের Chat ID দিন (মাইনাস সহ)
GEMINI_API_KEY = "AQ.Ab8RN6LL6bo572E7Dnn58pRlRKFIhjA6b-DDSyXY1bt5TMiTbw"  # আপনার Gemini API Key দিন

# ইনিশিয়ালাইজেশন
bot = Bot(token=BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# Gemini Flash দিয়ে Telegram Tips জেনারেট করার ফাংশন
def generate_telegram_tip():
    prompt = (
        "Generate a short, extremely helpful Telegram tip or feature secret for users. "
        "Keep it concise, engaging, under 250 characters, and use appropriate emojis. "
        "Write in simple English or Bangla suitable for a Telegram community."
    )
    
    # Gemini 1.5 Flash মডেল ব্যবহার
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()

# অটোমেটিক AI মেসেজ পাঠানোর ব্যাকগ্রাউন্ড টাস্ক
async def auto_send_ai_tips():
    while True:
        try:
            # ১. Gemini থেকে টিপস জেনারেট
            tip_content = generate_telegram_tip()
            
            # ২. মেসেজের ফরম্যাট সাজানো
            full_message = f"💡 **Telegram Tip of the Day** 💡\n\n{tip_content}"
            
            # ৩. টেলিগ্রাম গ্রুপে পাঠানো
            await bot.send_message(chat_id=CHAT_ID, text=full_message, parse_mode="Markdown")
            print("[SUCCESS] Gemini Flash AI থেকে টিপস তৈরি করে সফলভাবে পাঠানো হয়েছে।")
            
        except TelegramError as e:
            print(f"[ERROR] Telegram সার্ভিস এরর: {e}")
        except Exception as e:
            print(f"[ERROR] Gemini API বা অন্যান্য সমস্যা: {e}")
            
        # প্রতি ৩৬০০ সেকেন্ড (১ ঘণ্টা) পর পর পাঠাবে
        await asyncio.sleep(3600)

# Lifespan ইভেন্ট
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(auto_send_ai_tips())
    yield
    task.cancel()

app = FastAPI(title="Gemini AI Telegram Tips Bot", lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "running", "bot": "Gemini Flash Auto Tips Bot Active"}
