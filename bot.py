from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

users = {}

# القائمة الرئيسية
main_menu = [
    ["👤 حسابي", "💼 محفظة"],
    ["🔗 دعوة أصدقاء", "🎁 مهام"],
    ["🎉 مكافأة يومية"]
]

reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        users[user_id] = {"balance": 0}

    await update.message.reply_text(
        "أهلاً بك في بوت Mafhumatk 👋",
        reply_markup=reply_markup
    )

# التعامل مع الأزرار
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "👤 حسابي":
        await update.message.reply_text(f"🆔 ID: {user_id}")

    elif text == "💼 محفظة":
        balance = users[user_id]["balance"]
        await update.message.reply_text(f"💰 رصيدك: {balance}")

    elif text == "🔗 دعوة أصدقاء":
        link = f"https://t.me/Mafhumatk_bot?start={user_id}"
        await update.message.reply_text(f"🔗 رابط الدعوة:\n{link}")

    elif text == "🎁 مهام":
        await update.message.reply_text("📌 قريباً سيتم إضافة مهام")

    elif text == "🎉 مكافأة يومية":
        users[user_id]["balance"] += 5
        await update.message.reply_text("🎉 تم إضافة 5 نقاط لرصيدك")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, menu_handler))

app.run_polling()
