import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from telegram import Bot
from telegram.error import TelegramError
from groq import Groq

# --- কনফিগারেশন ---
BOT_TOKEN = "8680178701:AAEdRETzMseHbOZuMmQFXpR9RemM-CQ8dl0"  # বটের টোকেন দিন
CHAT_ID = "-1002352180501"                  # গ্রুপের Chat ID (মাইনাস সহ)
GROQ_API_KEY = "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"      # Groq API Key দিন

# ইনিশিয়ালাইজেশন
bot = Bot(token=BOT_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)

# ব্যবহারযোগ্য Groq মডেলগুলোর তালিকা (অগ্রাধিকার ক্রমানুসারে)
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
    "mixtral-8x7b-32768"
]

# Groq API দিয়ে Telegram Tips জেনারেট করার ডায়নামিক ফাংশন
def generate_telegram_tip():
    prompt = (
        "Generate a short, extremely helpful Telegram tip or feature secret for users. "
        "Keep it concise, engaging, under 250 characters, and use appropriate emojis. "
        "Write in simple English or Bangla suitable for a Telegram community."
    )
    
    # তালিকায় থাকা মডেলগুলো দিয়ে একে একে ট্রাই করবে
    for model_name in AVAILABLE_MODELS:
        try:
            response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a Telegram power-user expert providing daily short tips."},
                    {"role": "user", "content": prompt}
                ],
                model=model_name,
                temperature=0.7,
                max_tokens=150
            )
            print(f"[INFO] সফলভাবে {model_name} মডেল ব্যবহার করা হয়েছে।")
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[WARNING] {model_name} মডেলে সমস্যা দেখা দিয়েছে: {e}। পরবর্তী মডেলে চেষ্টা করা হচ্ছে...")
            continue
            
    raise Exception("Groq-এর কোনো মডেলই বর্তমানে কাজ করছে না। API Key এবং মডেল স্ট্যাটাস চেক করুন।")

# অটোমেটিক AI মেসেজ পাঠানোর ব্যাকগ্রাউন্ড টাস্ক
async def auto_send_ai_tips():
    while True:
        try:
            tip_content = generate_telegram_tip()
            full_message = f"💡 **Telegram Tip of the Day** 💡\n\n{tip_content}"
            
            await bot.send_message(chat_id=CHAT_ID, text=full_message, parse_mode="Markdown")
            print("[SUCCESS] Groq AI থেকে টিপস তৈরি করে টেলিগ্রাম গ্রুপে পাঠানো হয়েছে।")
            
        except TelegramError as e:
            print(f"[ERROR] Telegram সার্ভিস এরর: {e}")
        except Exception as e:
            print(f"[ERROR] Groq API বা মেসেজ প্রসেসিং এরর: {e}")
            
        # প্রতি ৩৬০০ সেকেন্ড (১ ঘণ্টা) পর পর মেসেজ পাঠাবে
        await asyncio.sleep(3600)

# Lifespan ইভেন্ট
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(auto_send_ai_tips())
    yield
    task.cancel()

app = FastAPI(title="Groq AI Telegram Tips Bot", lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "running", "bot": "Groq AI Auto Tips Bot with Fallback system is active"}
