import os
from dotenv import load_dotenv

load_dotenv()

# ===== TELEGRAM BOT CONFIG =====
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN", "")
TELEGRAM_WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL", "")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", 8080))
OWNER_ID = int(os.getenv("OWNER_ID", 0))
LOGGER_ID = int(os.getenv("LOGGER_ID", 0))  # -1003858465326

# ===== PYROGRAM CLIENT CONFIG (String Session) =====
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")
BOT_NAME = os.getenv("BOT_NAME", "🎵 MUSIC BOT")

# ===== OPENAI (ChatGPT) CONFIG =====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# ===== MONGODB CONFIG =====
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "music_bot")

# ===== SPOTIFY CONFIG =====
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")

# ===== YOUTUBE CONFIG =====
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

# ===== BOT SETTINGS =====
DEFAULT_QUEUE_LIMIT = int(os.getenv("DEFAULT_QUEUE_LIMIT", 50))
MAX_SONG_DURATION = int(os.getenv("MAX_SONG_DURATION", 3600))  # 1 hour
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/song_assistant")

# Group management
ADMIN_COMMANDS = [
    "clear_queue",
    "ban_user",
    "unban_user",
    "set_prefix",
    "toggle_max_duration"
]

# ===== LOGGING & DEBUG =====
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_CHANNEL = LOGGER_ID  # Send logs to this channel
