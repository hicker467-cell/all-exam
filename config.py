import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "all_exams_db"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AI_MODEL = "openai/gpt-oss-120b"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

COACHING_NAME = os.getenv("COACHING_NAME", "Sagar Coaching Centre, Bhagwanpur")
COACHING_PHONE = os.getenv("COACHING_PHONE", "+91 91101 13671")
COACHING_YOUTUBE = os.getenv("COACHING_YOUTUBE", "https://www.youtube.com/@sagarcoachingcentrebhagwanpur")
COACHING_TELEGRAM = os.getenv("COACHING_TELEGRAM", "https://t.me/ShrvanKumarSagar")

# Headers for HTTP scraping
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
    "Connection": "keep-alive"
}
