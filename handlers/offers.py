from telegram import Update
from telegram.ext import ContextTypes

async def offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎁 العروض ستتوفر قريبًا 🔥"
    )
