import telebot
import os
from modules.tasks.tasks import register_tasks
from database import get_connection

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# تسجيل المستخدم
@bot.message_handler(commands=['start'])
def start(msg):
    user_id = msg.from_user.id

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO users (user_id) VALUES (%s) ON CONFLICT DO NOTHING", (user_id,))
    conn.commit()

    cur.close()
    conn.close()

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("المهام")

    bot.send_message(msg.chat.id, "👋 أهلاً بك\n👇 اختر من القائمة", reply_markup=keyboard)

# زر المهام
@bot.message_handler(func=lambda msg: msg.text == "المهام")
def tasks_menu(msg):
    from modules.tasks.tasks import show_tasks
    show_tasks(bot, msg)

# تسجيل نظام المهام
register_tasks(bot)

print("✅ USER BOT RUNNING...")
bot.infinity_polling()
