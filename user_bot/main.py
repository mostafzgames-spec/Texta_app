import os
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram import F
from aiogram.types import Message
from sqlalchemy import select

from shared.database.connection import SessionLocal, engine
from shared.database.models import Base, User

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = FastAPI()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# إنشاء الجداول
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Webhook URL من Railway
    WEBHOOK_URL = os.getenv("RAILWAY_STATIC_URL")

    if not WEBHOOK_URL:
        print("❌ RAILWAY_STATIC_URL مش موجود")
        return

    webhook = f"https://{WEBHOOK_URL}"

    await bot.set_webhook(webhook)
    print("Webhook set:", webhook)


# استقبال التحديثات
@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}


# /start
@dp.message(F.text == "/start")
async def start_handler(message: Message):
    async with SessionLocal() as session:
        telegram_id = message.from_user.id

        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            new_user = User(telegram_id=telegram_id)
            session.add(new_user)
            await session.commit()

            await message.answer("👋 أهلاً بيك، تم تسجيلك!")
            return

        await message.answer(f"👋 رجعت تاني\n💰 رصيدك: {user.balance}")


# fallback
@dp.message()
async def echo(message: Message):
    await message.answer("📩 وصلي كلامك")
