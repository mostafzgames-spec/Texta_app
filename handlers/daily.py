from telegram import Update
from telegram.ext import ContextTypes
from database import get_last_daily, update_daily, add_balance
import time

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    last_time = get_last_daily(user_id)
    now = int(time.time())

    if now - last_time < 86400:
        await update.message.reply_text("❌ استلمت المكافأة اليوم بالفعل")
    else:
        add_balance(user_id, 5)
        update_daily(user_id, now)
        await update.message.reply_text("🎉 تم إضافة 5 نقاط")
