import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message

from user_bot.handlers.start import router
from shared.database.connection import engine
from user_bot.db.base import Base

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # حذف webhook
    await bot.delete_webhook(drop_pending_updates=True)

    # ربط الهاندلر
    dp.include_router(router)

    # fallback بسيط (مش بيأثر على start)
    @dp.message()
    async def echo(message: Message):
        print("Message received:", message.text)
        await message.answer("📩 وصلني كلامك")

    # إنشاء الجداول
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Bot is running...")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
