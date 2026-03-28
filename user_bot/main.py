import telebot
from config import BOT_TOKEN
from init_db import create_tables

from modules.account.account import register_account
from modules.tasks.tasks import register_tasks
from modules.referral.referral import register_referral

bot = telebot.TeleBot(BOT_TOKEN)

create_tables()

register_account(bot)
register_tasks(bot)
register_referral(bot)

print("User bot running...")
bot.infinity_polling()
