import os
from pathlib import Path
from pydantic_settings import BaseSettings

# প্রজেক্টের রুট ডিরেক্টরি (Root Directory) পাথ নির্ধারণ
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # প্রজেক্টের সাধারণ সেটিংস
    PROJECT_NAME: str = "FastAPI App"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # ডেটাবেস ও সিকিউরিটি সেটিংস (প্রয়োজন অনুযায়ী পরিবর্তন করুন)
    # SECRET_KEY: str = "your-secret-key-here"
    # DATABASE_URL: str = "sqlite:///./sql_app.db"

    class Config:
        # .env ফাইল থাকলে তা স্বয়ংক্রিয়ভাবে লোড করবে
        env_file = os.path.join(BASE_DIR, ".env")
        case_sensitive = True

# সেটিংস ইনস্ট্যান্স তৈরি
settings = Settings()
