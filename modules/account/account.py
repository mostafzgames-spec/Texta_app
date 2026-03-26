from telegram import Update
from telegram.ext import ContextTypes
from modules.account.account_db import get_user_data

async def account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user_data(user_id)

    if user:
        user_id, join_date = user
        date, time = join_date.split(" ")
    else:
        date, time = "غير معروف", "غير معروف"

    await update.message.reply_text(
        f"👤 حسابك:\n\n"
        f"🆔 ID: {user_id}\n\n"
        f"📅 التاريخ: {date}\n"
        f"🕒 الوقت: {time}"
    )
