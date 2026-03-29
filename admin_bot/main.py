import telebot
import os
import sys

# حل الاستيراد
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from admin_bot.config import ADMIN_BOT_TOKEN
from modules.tasks.add_task import register_add_task

bot = telebot.TeleBot(ADMIN_BOT_TOKEN)

# تسجيل النظام
register_add_task(bot)

print("Admin bot running...")

bot.infinity_polling()
