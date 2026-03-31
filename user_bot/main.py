import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    @dp.message()
    async def echo(message: Message):
        print("Message received:", message.text)
        await message.answer("🔥 البوت شغال!")

    print("Bot is running...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
