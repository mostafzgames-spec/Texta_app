import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from handlers.start import start
from handlers.account import account
from handlers.wallet import wallet
from handlers.referral import referral
from handlers.tasks import tasks
from handlers.daily import daily
from handlers.support import support
from handlers.logs import logs
from handlers.leaderboard import leaderboard

TOKEN = os.getenv("TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(MessageHandler(filters.Regex("👤 حسابي"), account))
app.add_handler(MessageHandler(filters.Regex("💼 محفظة"), wallet))
app.add_handler(MessageHandler(filters.Regex("🔗 دعوة أصدقاء"), referral))
app.add_handler(MessageHandler(filters.Regex("🎁 مهام"), tasks))
app.add_handler(MessageHandler(filters.Regex("🎉 مكافأة يومية"), daily))
app.add_handler(MessageHandler(filters.Regex("☎️ خدمة العملاء"), support))
app.add_handler(MessageHandler(filters.Regex("📜 سجلاتي"), logs))
app.add_handler(MessageHandler(filters.Regex("🏆 المتصدرين"), leaderboard))

app.run_polling()
