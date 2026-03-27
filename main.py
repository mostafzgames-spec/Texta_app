import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# إنشاء الجداول
from init_db import create_tables
create_tables()

# الموديولات الجديدة
from modules.account.account import account
from modules.referral.referral import referral
from modules.tasks.tasks import tasks, handle_task

# باقي القوائم
from handlers.start import start
from handlers.wallet import wallet_menu
from handlers.daily import daily
from handlers.support import support
from handlers.logs import logs
from handlers.leaderboard import leaderboard
from handlers.stats import stats
from handlers.channel import channel
from handlers.offers import offers
from handlers.withdraw import withdraw
from handlers.balance import balance

TOKEN = os.getenv("TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

# أمر البداية
app.add_handler(CommandHandler("start", start))

# القوائم الأساسية
app.add_handler(MessageHandler(filters.Regex("👤 حسابي"), account))
app.add_handler(MessageHandler(filters.Regex("💼 محفظة"), wallet_menu))
app.add_handler(MessageHandler(filters.Regex("📊 إحصائياتي"), stats))
app.add_handler(MessageHandler(filters.Regex("🔗 دعوة أصدقاء"), referral))
app.add_handler(MessageHandler(filters.Regex("🎁 مهام"), tasks))
app.add_handler(MessageHandler(filters.Regex("🎉 مكافأة يومية"), daily))
app.add_handler(MessageHandler(filters.Regex("📢 قناتنا"), channel))
app.add_handler(MessageHandler(filters.Regex("🎁 العروض"), offers))
app.add_handler(MessageHandler(filters.Regex("☎️ خدمة العملاء"), support))
app.add_handler(MessageHandler(filters.Regex("📜 السجلات"), logs))
app.add_handler(MessageHandler(filters.Regex("🏆 المتصدرين"), leaderboard))

# داخل المحفظة
app.add_handler(MessageHandler(filters.Regex("💰 رصيدي"), balance))
app.add_handler(MessageHandler(filters.Regex("💳 سحب الأرباح"), withdraw))

# نظام المهام (الأزرار التفاعلية)
app.add_handler(CallbackQueryHandler(handle_task))

app.run_polling()
