import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

from user_bot.handlers.start import router
from shared.database.connection import engine
from user_bot.db.base import Base

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # ربط الهاندلر الأساسي
    dp.include_router(router)

    # fallback لأي رسالة (بس مش /start)
    @dp.message()
    async def echo(message: Message):
        if message.text.startswith("/start"):
            return
        print("Message received:", message.text)
        await message.answer("📩 وصلني كلامك")

    # إنشاء الجداول
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Bot is running...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
