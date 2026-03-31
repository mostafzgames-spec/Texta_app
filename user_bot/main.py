import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Start command
    @dp.message(CommandStart())
    async def start_handler(message: Message):
        print("User pressed start")
        await message.answer("👋 أهلاً بيك في بوت Mafhumatk")

    # Test أي رسالة
    @dp.message()
    async def echo(message: Message):
        print("Message received:", message.text)
        await message.answer("📩 وصلني كلامك")

    print("Bot is running...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
