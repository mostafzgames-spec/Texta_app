import telebot
import os
import sys

# حل مشكلة الاستيراد بين المجلدات
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from admin_bot.config import ADMIN_BOT_TOKEN

# استدعاء الموديولز
from modules.tasks.add_task import register_add_task
from modules.broadcast import broadcast

# إنشاء البوت
bot = telebot.TeleBot(ADMIN_BOT_TOKEN)

# تسجيل الأنظمة
register_add_task(bot)
broadcast.register_broadcast(bot)

print("Admin bot running...")

# تشغيل البوت
bot.infinity_polling()
