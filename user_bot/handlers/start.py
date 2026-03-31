from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def start_handler(message: Message):
    if message.text == "/start":
        print("Start triggered")
        await message.answer("👋 أهلاً بيك في بوت Mafhumatk")
