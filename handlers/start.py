from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import add_user
from modules.referral.referral_db import set_referrer

main_menu = [
    ["👤 حسابي", "💼 محفظة"],
    ["📊 إحصائياتي", "🎁 مهام"],
    ["🔗 دعوة أصدقاء", "🎉 مكافأة يومية"],
    ["📢 قناتنا", "🎁 العروض"],
    ["☎️ خدمة العملاء", "📜 السجلات"],
    ["🏆 المتصدرين"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    invited_by = int(context.args[0]) if context.args else None

    # إضافة المستخدم
    add_user(user_id, invited_by)

    # ربط الدعوة
    if invited_by and invited_by != user_id:
        set_referrer(user_id, invited_by)

    await update.message.reply_text(
        "أهلاً بك في Mafhumatk 👋",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )
