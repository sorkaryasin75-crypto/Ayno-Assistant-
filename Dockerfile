# ১. পাইথন ৩.১২-এর অফিশিয়াল লাইটওয়েট ইমেজ ব্যবহার
FROM python:3.12-slim

# ২. ওয়ার্কিং ডিরেক্টরি সেট করা
WORKDIR /app

# ৩. পাইথন ক্যাশ বন্ধ করা এবং এনভায়রনমেন্ট সেটআপ
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# ৪. প্রয়োজনীয় সিস্টেম ডিপেন্ডেন্সি ইনস্টল
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ৫. ডিপেন্ডেন্সি কপি ও ইনস্টল
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ৬. প্রজেক্ট ফাইল কপি করা
COPY . .

# ৭. পোর্ট এক্সপোজ করা
EXPOSE 8000

# ৮. Uvicorn দিয়ে FastAPI সার্ভার রান করা
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
