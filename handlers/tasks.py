from telegram import Update
from telegram.ext import ContextTypes

async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📌 المهام سيتم إضافتها قريباً")
