from telegram import Update
from telegram.ext import ContextTypes
import sqlite3

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, balance FROM users ORDER BY balance DESC LIMIT 5")
    top_users = cursor.fetchall()

    text = "🏆 المتصدرين:\n\n"

    for i, user in enumerate(top_users, start=1):
        text += f"{i}- {user[0]} | 💰 {user[1]}\n"

    await update.message.reply_text(text)
