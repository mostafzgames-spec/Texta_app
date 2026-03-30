import telebot
import os

from modules.tasks.tasks import register_tasks

# ✅ التوكن من Railway
BOT_TOKEN = os.getenv("USER_BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("❌ USER_BOT_TOKEN مش موجود في Environment Variables")

# ✅ إنشاء البوت
bot = telebot.TeleBot(BOT_TOKEN)

# 🔥 حل مشكلة Conflict (مهم جدًا)
bot.remove_webhook()

# 📌 رسالة البداية
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 أهلاً بك\n\nاختر من القائمة 👇"
    )

# 📌 تسجيل نظام المهام
register_tasks(bot)

# 🚀 تشغيل البوت
print("✅ User Bot Started...")
bot.infinity_polling()
