import telebot
import os
import sys
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# 🔥 الحل هنا
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from modules.tasks.tasks import register_tasks

BOT_TOKEN = os.getenv("USER_BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# تسجيل نظام المهام
register_tasks(bot)

# قائمة رئيسية
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    btn_tasks = KeyboardButton("المهام")
    markup.add(btn_tasks)

    bot.send_message(
        message.chat.id,
        "👋 أهلاً بك",
        reply_markup=markup
    )

print("User bot running...")

bot.infinity_polling()
