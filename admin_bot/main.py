import telebot
import os
import sys

# مهم عشان يقرأ modules اللي بره
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from admin_bot.config import ADMIN_BOT_TOKEN

# استدعاء الأنظمة
from modules.tasks.add_task import register_add_task
from modules.broadcast import register_broadcast

bot = telebot.TeleBot(ADMIN_BOT_TOKEN)

# تشغيل الأنظمة
register_add_task(bot)
register_broadcast(bot)

print("Admin bot running...")

bot.infinity_polling()
