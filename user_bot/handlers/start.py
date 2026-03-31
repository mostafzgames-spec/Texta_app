from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from shared.database.connection import SessionLocal
from user_bot.db.user_model import User
from sqlalchemy import select

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar()

        if not user:
            new_user = User(telegram_id=message.from_user.id)
            session.add(new_user)
            await session.commit()

    await message.answer("👋 أهلاً بيك في بوت Mafhumatk")
