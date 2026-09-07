import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from telegram import Bot
from telegram.error import TelegramError

# --- কনফিগারেশন ---
BOT_TOKEN = "8680178701:AAEdRETzMseHbOZuMmQFXpR9RemM-CQ8dl0"  # আপনার বট টোকেন দিন
CHAT_ID = "-1002352180501"  # আপনার টেলিগ্রাম গ্রুপের CHAT ID দিন (অবশ্যই মাইনাস সহ)

bot = Bot(token=BOT_TOKEN)

# অটোমেটিক মেসেজ পাঠানোর ব্যাকগ্রাউন্ড টাস্ক
async def auto_send_messages():
    while True:
        try:
            # গ্রুপে পাঠানো মেসেজের তথ্য
            message_text = "🤖 এটি সিস্টেম থেকে পাঠানো অটোমেটিক মেসেজ!"
            
            await bot.send_message(chat_id=CHAT_ID, text=message_text)
            print("[SUCCESS] গ্রুপে মেসেজ সফলভাবে পাঠানো হয়েছে।")
            
        except TelegramError as e:
            print(f"[ERROR] মেসেজ পাঠাতে সমস্যা হয়েছে: {e}")
        except Exception as e:
            print(f"[ERROR] অজানা সমস্যা: {e}")
            
        # প্রতি কত সেকেন্ড পর পর মেসেজ পাঠাতে চান (এখানে ৬০ সেকেন্ড দেওয়া আছে)
        await asyncio.sleep(60)

# Lifespan ইভেন্ট (FastAPI সার্ভার চালু ও বন্ধ হওয়ার সময় রান করবে)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # সার্ভার চালু হওয়ার সাথে সাথে ব্যাকগ্রাউন্ড টাস্ক শুরু হবে
    task = asyncio.create_task(auto_send_messages())
    yield
    # সার্ভার বন্ধ হলে টাস্ক ক্যানসেল হবে
    task.cancel()

app = FastAPI(title="Telegram Auto Notifier", lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "running", "message": "Telegram Auto Notifier System Active"}
