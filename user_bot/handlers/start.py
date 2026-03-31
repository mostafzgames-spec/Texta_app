from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message):
    print("Start command received")
    await message.answer("👋 أهلاً بيك في بوت Mafhumatk")
