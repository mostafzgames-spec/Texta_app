import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    print("Bot starting...")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # مهم جداً
    await bot.delete_webhook(drop_pending_updates=True)

    @dp.message()
    async def all_messages(message: Message):
        print("وصلت رسالة:", message.text)

        if message.text == "/start":
            await message.answer("👋 أهلاً بيك")
        else:
            await message.answer("📩 شغال تمام")

    print("Bot is running...")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
