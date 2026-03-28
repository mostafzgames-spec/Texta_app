import telebot
import os
import sys

# حل مشكلة الاستيراد من خارج المجلد
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from init_db import create_tables
from config import BOT_TOKEN

from modules.account.account import register_account
from modules.tasks.tasks import register_tasks
from modules.referral.referral import register_referral

bot = telebot.TeleBot(BOT_TOKEN)

# إنشاء الجداول
create_tables()

# تسجيل الموديولز
register_account(bot)
register_tasks(bot)
register_referral(bot)

print("User bot running...")
bot.infinity_polling()
