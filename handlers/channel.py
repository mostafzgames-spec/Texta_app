from telegram import Update
from telegram.ext import ContextTypes

async def channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📢 تابع قناتنا:\nhttps://t.me/Mafhumatk"
    )
