import sys
import os

# ✅ حل مشكلة modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from modules.tasks.tasks import register_tasks

# ✅ التوكن من Railway
BOT_TOKEN = os.getenv("USER_BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("❌ USER_BOT_TOKEN مش موجود في Environment Variables")

# ✅ إنشاء البوت
bot = telebot.TeleBot(BOT_TOKEN)

# 🔥 حل مشكلة Conflict
bot.remove_webhook()

# 📌 أمر /start + إظهار قائمة
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    # زر المهام
    btn_tasks = KeyboardButton("المهام")
    markup.add(btn_tasks)

    bot.send_message(
        message.chat.id,
        "👋 أهلاً بك\n\nاختر من القائمة 👇",
        reply_markup=markup
    )

# 📌 تسجيل نظام المهام
register_tasks(bot)

# 🚀 تشغيل البوت
print("✅ User Bot Started...")
bot.infinity_polling()
