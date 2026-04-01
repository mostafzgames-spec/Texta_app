import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message

BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")

ADMIN_ID = int(os.getenv("ADMIN_ID"))

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)

    @dp.message()
    async def handler(message: Message):
        if message.from_user.id != ADMIN_ID:
            return

        if message.text == "/start":
            await message.answer("🛠️ لوحة الأدمن جاهزة")

        elif message.text == "ping":
            await message.answer("🏓 admin bot شغال")

    print("Admin bot running...")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
