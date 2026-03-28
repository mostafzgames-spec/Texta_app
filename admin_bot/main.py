import telebot
import os
import sys

# حل مشكلة الاستيراد بين المجلدات
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from admin_bot.config import ADMIN_BOT_TOKEN
from modules.tasks.add_task import register_add_task
from modules.broadcast.broadcast import register_broadcast

# إنشاء البوت
bot = telebot.TeleBot(ADMIN_BOT_TOKEN)

# تسجيل الموديولز
register_add_task(bot)
register_broadcast(bot)

print("Admin bot running...")

# تشغيل البوت
bot.infinity_polling()
