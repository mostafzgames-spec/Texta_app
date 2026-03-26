from telegram import Update
from telegram.ext import ContextTypes

async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 سجلاتك\n\n"
        "سيتم عرض العمليات هنا قريبًا 🔥"
    )
