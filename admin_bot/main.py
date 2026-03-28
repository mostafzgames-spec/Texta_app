import telebot
import os
import sys

# حل نفس المشكلة هنا
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import BOT_TOKEN
from modules.tasks.add_task import register_add_task

bot = telebot.TeleBot(BOT_TOKEN)

register_add_task(bot)

print("Admin bot running...")
bot.infinity_polling()
