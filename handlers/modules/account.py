from telegram import Update
from telegram.ext import ContextTypes
from database import get_join_date

async def account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    join_date = get_join_date(user_id)

    # تقسيم التاريخ والوقت
    date, time = join_date.split(" ")

    await update.message.reply_text(
        f"👤 حسابك:\n\n"
        f"🆔 ID: {user_id}\n\n"
        f"📅 التاريخ: {date}\n"
        f"🕒 الوقت: {time}"
    )
