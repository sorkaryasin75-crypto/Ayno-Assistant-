import asyncio
import random
from contextlib import asynccontextmanager
from fastapi import FastAPI
from telegram import Bot
from telegram.error import TelegramError

# --- কনফিগারেশন ---
BOT_TOKEN = "8680178701:AAEdRETzMseHbOZuMmQFXpR9RemM-CQ8dl0"  # আপনার বট টোকেন দিন
CHAT_ID = "-1002352180501"  # আপনার টেলিগ্রাম গ্রুপের CHAT ID দিন (অবশ্যই মাইনাস সহ)

bot = Bot(token=BOT_TOKEN)

# --- Tech & Online Earning Tips Collection ---
TECH_EARNING_TIPS = [
    # 💻 Freelancing & Skills
    "💻 Tech Tip: ফুল-স্ট্যাক ওয়েব ডেভেলপমেন্টের জন্য HTML, CSS, JavaScript, React এবং Node.js শেখা শুরু করতে পারেন।",
    "💼 Earning Tip: ফ্রিল্যান্সিংয়ে ক্লায়েন্ট পাওয়ার জন্যUpwork ও Fiverr-এর পাশাপাশি LinkedIn প্রফেশনাল প্রোফাইল ব্যবহার করুন।",
    "💻 Tech Tip: AI tools যেমন ChatGPT এবং GitHub Copilot কোডিংয়ের গতি ২x পর্যন্ত বাড়িয়ে দিতে পারে।",
    "💼 Earning Tip: Content Writing, Graphics Design এবং SEO হলো দ্রুত ফ্রিল্যান্সিং ইনকাম শুরু করার চমৎকার স্কিল।",
    "💻 Tech Tip: প্রোগ্রামিং শেখে শুরু করতে Python সেরা ভাষা, কারণ এর সিনট্যাক্স অনেক সহজ ও শিক্ষণীয়।",
    "💼 Earning Tip: Upwork-এ কভার লেটার লেখার সময় ক্লায়েন্টের সমস্যার সমাধান কীভাবে করবেন সেটিতে জোর দিন।",
    "💻 Tech Tip: আপনার কোডের ব্যাকআপ রাখতে এবং পোর্টফোলিও তৈরি করতে নিয়মিত GitHub ব্যবহার করুন।",
    "💼 Earning Tip: ডিজিটাল মার্কেটিং শিখে ছোট স্থানীয় ব্যবসাগুলোর সোশ্যাল মিডিয়া ম্যানেজ করে মাসে ভালো আয় সম্ভব।",
    "💻 Tech Tip: সাইবার সিকিউরিটিতে ক্যারিয়ার গড়তে Ethical Hacking এবং Networking fundamentals জানা জরুরি।",
    "💼 Earning Tip: ক্লায়েন্ট রিটেনশন বাড়াতে কাজের ডিক্লেয়ার্ড ডেডলাইনের অন্তত ১ দিন আগে প্রজেক্ট ডেলিভারি দেওয়ার চেষ্টা করুন।",

    # 🚀 Micro SaaS & Monetization
    "🚀 Earning Strategy: ছোট একটি સમસ્યા সমাধান করে Micro-SaaS তৈরি করুন এবং মান্থলি সাবস্ক্রিপশন মডেলে আয় করুন।",
    "💡 Tech Tip: No-Code টুলస్ যেমন Bubble বা Webflow ব্যবহার করে কোডিং ছাড়াই ওয়েব অ্যাপ বানানো সম্ভব।",
    "🚀 Earning Strategy: আপনার কোডের পুনঃব্যবহারযোগ্য কাস্টম কম্পোনেন্ট বা টেমপ্লেট Envato / CodeCanyon-এ বিক্রি করতে পারেন।",
    "💡 Tech Tip: Cloud Hosting-এর জন্য Vercel, Netlify বা Render ব্যবহার করে ফ্রিতে প্রজেক্ট হোস্ট করতে পারেন।",
    "🚀 Earning Strategy: টেলিগ্রাম গ্রুপ Moderation Bot বা Crypto Alert Bot বানিয়ে পেইড বট হিসেবে মাসিক চার্জ করুন।",

    # 📱 Affiliate & Content Monetization
    "💰 Passive Income: নির্দিষ্ট নিশের (Niche) ওপর রিভিউ ব্লগ সাইট বানিয়ে Amazon Affiliate Marketing থেকে প্যাসিভ ইনকাম করুন।",
    "🎥 Tech Earning: টেক টিউটোরিয়াল বা কোডিং প্রবলেম সলভিং ভিডিও বানিয়ে YouTube থেকে Monetization পেতে পারেন।",
    "💰 Passive Income: আপনার তৈরি Digital Assets (3D models, UI Kits, eBooks) Gumroad-এ বিক্রি শুরু করুন।",
    "🎥 Tech Earning: টেকনোলজি সম্পর্কিত খবরের জন্য একটি টেলিগ্রাম চ্যানেল বানিয়ে স্পন্সরশিপের মাধ্যমে আয় করা সম্ভব।",
    "💰 Passive Income: নিবেদিত অডিয়েন্স থাকলে সাবস্ক্রিপশন ভিত্তিক মেম্বারশিপ বা Premium Telegram Channel চালু করুন।",

    # 🔐 Security & Tech Smart Tips
    "🛡️ Tech Security: আপনার সকল ফিন্যান্সিয়াল ও ফ্রিল্যান্সিং অ্যাকাউন্টে সবসময় 2FA (Two-Factor Authentication) অন রাখুন।",
    "🛠️ Tech Tip: API টেস্টিংয়ের জন্য Postman বা Bruno টুলস ব্যবহার করলে ডেভেলপারদের সময় অনেক বেঁচে যায়।",
    "🛡️ Tech Security: কখনো API Key বা Client Secret সরাসরি পাবলিক কোড রিপোজিটরিতে (GitHub) পুশ করবেন না।",
    "🛠️ Tech Tip: প্রজেক্ট ডাটাবেজ হিসেবে PostgreSQL বা Supabase ব্যবহার করা স্কেলেবল ও দ্রুতগতির সমাধান।",
    "🛡️ Tech Security: অপরিচিত কারো পাঠানো ফাইল (.exe / .bat) টেলিগ্রাম বা ডিসকর্ড থেকে ডাউনলোড করবেন না।",

    # 📈 Productivity & Career
    "📈 Career Advice: প্রতিদিন অন্তত ১ ঘণ্টা নতুন কোনো টেকনোলজি শিখতে ব্যয় করুন; এটি লং-টার্মে বড় রিটার্ন দেবে।",
    "🎯 Productivity: Pomodoro টেকনিক (২৫ মিনিট কাজ + ৫ মিনিট ব্রেক) মেনে কাজ করলে কাজের মনোযোগ বাড়ে।",
    "📈 Career Advice: শুধু কাজ না শিখে কীভাবে কমিউনিকেশন করতে হয় এবং ক্লায়েন্ট হ্যান্ডেল করতে হয় তা শিখুন।",
    "🎯 Productivity: Notion বা Trello অ্যাপ দিয়ে প্রতিদিনের কাজের তালিকা টু-ডু (To-Do List) হিসেবে পরিচালনা করুন।"
]

# ১০০০+ অটো-মেসেজ চক্র সচল রাখার জন্য ডাইনামিক ফিলিং
for i in range(len(TECH_EARNING_TIPS) + 1, 501):
    tip_category = random.choice(["💻 Tech Tip", "💼 Earning Tip", "💡 Tech Strategy", "🚀 Passive Income"])
    TECH_EARNING_TIPS.append(f"{tip_category} #{i}: স্কিল ডেভেলপমেন্ট ও নিয়মিত অনুশীলনের মাধ্যমেই টেকনোলজি ও অনলাইন আর্নিংয়ে স্থায়ী সাফল্য সম্ভব।")


# অটোমেটিক মেসেজ পাঠানোর ব্যাকগ্রাউন্ড টাস্ক
async def auto_send_messages():
    while True:
        try:
            # র‍্যান্ডম টেক ও আর্নিং মেসেজ সিলেক্ট
            message_text = random.choice(TECH_EARNING_TIPS)
            
            await bot.send_message(chat_id=CHAT_ID, text=message_text)
            print("[SUCCESS] টেকনোলজি ও আর্নিং মেসেজ গ্রুপে পাঠানো হয়েছে।")
            
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

app = FastAPI(title="Tech & Earning Auto Notifier", lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "running", "message": "Tech & Earning Telegram Bot System Active"}
