from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

wallet_menu_buttons = [
    ["💰 رصيدي", "💳 سحب الأرباح"],
    ["🔙 رجوع"]
]

async def wallet_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💼 المحفظة:",
        reply_markup=ReplyKeyboardMarkup(wallet_menu_buttons, resize_keyboard=True)
    )
