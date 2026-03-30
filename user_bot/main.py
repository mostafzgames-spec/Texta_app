import telebot
import os
import sys

# 🔥 حل مشكلة modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.tasks.tasks import register_tasks, show_tasks
from database import get_connection

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("❌ BOT_TOKEN مش موجود في Environment Variables")

bot = telebot.TeleBot(BOT_TOKEN)

# ✅ تسجيل المستخدم
@bot.message_handler(commands=['start'])
def start(msg):
    user_id = msg.from_user.id

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (user_id)
        VALUES (%s)
        ON CONFLICT (user_id) DO NOTHING
    """, (user_id,))

    conn.commit()
    cur.close()
    conn.close()

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("المهام")

    bot.send_message(
        msg.chat.id,
        "👋 أهلاً بك\n👇 اختر من القائمة",
        reply_markup=keyboard
    )

# ✅ زر المهام
@bot.message_handler(func=lambda msg: msg.text == "المهام")
def tasks_menu(msg):
    try:
        show_tasks(bot, msg)
    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ في مشكلة في السيرفر\n{e}")

# ✅ تسجيل نظام المهام
register_tasks(bot)

print("✅ USER BOT RUNNING...")

bot.infinity_polling()
