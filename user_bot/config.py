import os

# Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Fix for asyncpg (important for Railway)
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+asyncpg://"
    )

# Optional: basic validation (عشان يمنع تشغيل البوت لو في مشكلة)
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN is not set")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set")
