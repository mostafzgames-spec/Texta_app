from telegram import Update
from telegram.ext import ContextTypes
from database import get_balance

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance = get_balance(user_id)

    await update.message.reply_text(f"💰 رصيدك: {balance}")
