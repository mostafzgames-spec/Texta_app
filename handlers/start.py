from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import add_user

main_menu = [
    ["👤 حسابي", "💼 محفظة"],
    ["🔗 دعوة أصدقاء", "🎁 مهام"],
    ["🎉 مكافأة يومية"],
    ["☎️ خدمة العملاء", "📜 سجلاتي"],
    ["🏆 المتصدرين"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    invited_by = int(context.args[0]) if context.args else None

    add_user(user_id, invited_by)

    await update.message.reply_text(
        "أهلاً بك في Mafhumatk 👋",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )
