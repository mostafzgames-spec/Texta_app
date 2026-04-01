import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from sqlalchemy import select

from shared.database.connection import SessionLocal, engine
from shared.database.models import Base, User

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # إنشاء الجداول
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # مهم جداً
    await bot.delete_webhook(drop_pending_updates=True)

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

    # أي رسالة تانية
    @dp.message()
    async def echo(message: Message):
        await message.answer("📩 وصلي كلامك")

    print("User bot running...")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
