import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from modules.tasks.tasks import register_tasks

BOT_TOKEN = "PUT_YOUR_TOKEN_HERE"

bot = telebot.TeleBot(BOT_TOKEN)

# تسجيل نظام المهام
register_tasks(bot)

# 📌 قائمة رئيسية
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
