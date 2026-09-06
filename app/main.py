from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="My FastAPI App")

# ১. সাধারণ JSON API এন্ডপয়েন্ট (REST API-র জন্য)
@app.get("/")
async def read_root():
    return {
        "status": "success",
        "message": "সিস্টেমটি jinja2 ছাড়াই সফলভাবে চালু হয়েছে!"
    }

# ২. যদি কোনো পেজে HTML সরাসরি দেখাতে চান (অপশনাল)
@app.get("/home", response_class=HTMLResponse)
async def home_page():
    return """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <title>হোম পেজ</title>
    </head>
    <body>
        <h1>FastAPI সার্ভার সফলভাবে চলছে</h1>
        <p>এটি jinja2 টেমপ্লেটিং ইঞ্জিন ছাড়াই রেন্ডার করা হয়েছে।</p>
    </body>
    </html>
    """
