from telegram import Update
from telegram.ext import ContextTypes

async def account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(f"🆔 ID: {user_id}")
