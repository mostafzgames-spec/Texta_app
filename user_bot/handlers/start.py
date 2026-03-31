from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    print("User pressed start")
    await message.answer("👋 أهلاً بيك في بوت Mafhumatk")
