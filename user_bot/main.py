import asyncio
from aiogram import Bot, Dispatcher
from user_bot.config import BOT_TOKEN
from user_bot.handlers.start import router
from shared.database.connection import engine
from user_bot.db.base import Base

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
