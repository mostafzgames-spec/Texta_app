import telebot
import os
from init_db import create_tables
from start import register_start
from tasks import register_tasks

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# إنشاء الجداول
create_tables()

# تسجيل الهاندلرز
register_start(bot)
register_tasks(bot)

print("User bot running...")
bot.infinity_polling()
