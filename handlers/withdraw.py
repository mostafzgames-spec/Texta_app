from telegram import Update
from telegram.ext import ContextTypes
from database import get_balance

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bal = get_balance(user_id)

    if bal < 100:
        await update.message.reply_text("❌ الحد الأدنى للسحب 100 نقطة")
    else:
        await update.message.reply_text("✅ تم إرسال طلب السحب (سيتم مراجعته)")
