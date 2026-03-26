from telegram import Update
from telegram.ext import ContextTypes
import sqlite3

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE invited_by=?", (user_id,))
    invites = cursor.fetchone()[0]

    cursor.execute("SELECT balance FROM users WHERE id=?", (user_id,))
    balance = cursor.fetchone()[0]

    await update.message.reply_text(
        f"📊 إحصائياتك:\n\n"
        f"👥 الدعوات: {invites}\n"
        f"💰 رصيدك: {balance}"
    )
