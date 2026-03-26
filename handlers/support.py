from telegram import Update
from telegram.ext import ContextTypes

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "☎️ خدمة العملاء\n\n"
        "لو عندك مشكلة تواصل معانا:\n"
        "@Mafhumatk"
    )
