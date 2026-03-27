from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from modules.tasks.tasks_data import tasks_list
from modules.tasks.tasks_db import (
    can_do_task,
    save_task,
    can_do_new_task,
    update_last_task_time
)
from database import add_balance
from modules.referral.referral_db import add_referral_profit

import time

# حفظ وقت بدء المهمة
user_start_time = {}


# 🟢 عرض المهام (مختصر)
async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):

    for i, task in enumerate(tasks_list, start=1):

        text = (
            f"📢 مهمة {i} | 💰 {task['reward']} نقاط\n"
            f"📌 {task['name']}"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "ابدأ المهمة",
                    callback_data=f"start_{task['id']}"
                )
            ]
        ]

        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# 🟢 التعامل مع الأزرار
async def handle_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    # 🔹 بدء المهمة (عرض التفاصيل)
    if data.startswith("start_"):
        task_id = int(data.split("_")[1])

        # منع 3 دقائق
        if not can_do_new_task(user_id):
            await query.message.reply_text("⏳ لازم تستنى 3 دقائق قبل المهمة التالية")
            return

        # منع التكرار اليومي
        if not can_do_task(user_id, task_id):
            await query.message.reply_text("❌ عملت المهمة دي النهارده")
            return

        task = next(t for t in tasks_list if t["id"] == task_id)

        keyboard = [
            [InlineKeyboardButton("فتح الإعلان", url=task["link"])],
            [InlineKeyboardButton("✅ تم التنفيذ", callback_data=f"done_{task_id}")]
        ]

        user_start_time[user_id] = int(time.time())

        await query.message.reply_text(
            f"📢 {task['name']}\n\n"
            f"📝 {task['desc']}\n"
            f"💰 عدد النقاط: {task['reward']}\n\n"
            f"⏳ انتظر 20 ثانية ثم اضغط تم التنفيذ",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 🔹 إنهاء المهمة
    elif data.startswith("done_"):
        task_id = int(data.split("_")[1])

        if user_id not in user_start_time:
            await query.message.reply_text("❌ فشل التنفيذ")
            return

        start_time = user_start_time[user_id]
        now = int(time.time())

        # شرط 20 ثانية
        if now - start_time < 20:
            await query.message.reply_text("❌ لازم تنتظر 20 ثانية")
            return

        task = next(t for t in tasks_list if t["id"] == task_id)

        # إضافة النقاط
        add_balance(user_id, task["reward"])

        # أرباح الدعوة
        add_referral_profit(user_id, task["reward"])

        # حفظ التنفيذ
        save_task(user_id, task_id)

        # تحديث وقت آخر مهمة
        update_last_task_time(user_id)

        del user_start_time[user_id]

        await query.message.reply_text("✅ تم إضافة النقاط")
