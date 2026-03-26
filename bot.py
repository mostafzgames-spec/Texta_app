from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        users[user_id] = {"balance": 0}

    keyboard = [
        [InlineKeyboardButton("👤 حسابي", callback_data="account")],
        [InlineKeyboardButton("💰 رصيدي", callback_data="balance")],
        [InlineKeyboardButton("🔗 دعوة أصدقاء", callback_data="ref")]
    ]

    await update.message.reply_text("أهلا بيك 👋", reply_markup=InlineKeyboardMarkup(keyboard))


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "account":
        await query.message.reply_text(f"🆔 ID: {user_id}")

    elif query.data == "balance":
        await query.message.reply_text(f"💰 رصيدك: {users[user_id]['balance']}")

    elif query.data == "ref":
        link = f"https://t.me/YOUR_BOT_USERNAME?start={user_id}"
        await query.message.reply_text(f"🔗 رابط الدعوة:\n{link}")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
