from telegram import Update
from telegram.ext import ContextTypes

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    link = f"https://t.me/Mafhumatk_bot?start={user_id}"

    await update.message.reply_text(
        f"🔗 رابط الدعوة الخاص بك:\n\n{link}\n\n"
        f"💰 اربح 30٪ من أرباح كل صديق تدعوه"
    )
