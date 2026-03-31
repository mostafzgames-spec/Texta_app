import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message

from user_bot.handlers.start import router

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # ربط الهاندلر
    dp.include_router(router)

    # fallback لأي رسالة
    @dp.message()
    async def echo(message: Message):
        print("Message received:", message.text)
        await message.answer("📩 وصلني كلامك")

    print("Bot is running...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
