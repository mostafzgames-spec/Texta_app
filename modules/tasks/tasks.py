from database import get_connection
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

# تخزين مؤقت
user_task_time = {}

def register_tasks(bot):

    # 📌 عرض المهام
    @bot.message_handler(func=lambda msg: msg.text == "المهام")
    def show_tasks(message):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, title, reward FROM tasks")
        tasks = cur.fetchall()

        cur.close()
        conn.close()

        if not tasks:
            bot.send_message(message.chat.id, "❌ لا توجد مهام حالياً")
            return

        for i, task in enumerate(tasks, start=1):
            task_id, title, reward = task

            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton(
                    "🚀 فتح المهمة",
                    callback_data=f"start_{task_id}"
                )
            )

            bot.send_message(
                message.chat.id,
                f"📢 مهمة {i} | 💰 {reward} نقطة\n"
                f"📌 {title}",
                reply_markup=markup
            )

    # ▶️ فتح المهمة
    @bot.callback_query_handler(func=lambda call: call.data.startswith("start_"))
    def start_task(call):
        user_id = call.from_user.id
        task_id = int(call.data.split("_")[1])

        # تسجيل وقت البداية
        user_task_time[(user_id, task_id)] = time.time()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT link FROM tasks WHERE id=%s", (task_id,))
        task = cur.fetchone()

        cur.close()
        conn.close()

        if not task:
            bot.answer_callback_query(call.id, "❌ المهمة غير موجودة")
            return

        link = task[0]

        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🔗 فتح الرابط", url=link)
        )
        markup.add(
            InlineKeyboardButton("✅ تأكيد المهمة", callback_data=f"confirm_{task_id}")
        )

        bot.send_message(
            call.message.chat.id,
            "📌 افتح الرابط وانتظر 20 ثانية ثم اضغط تأكيد",
            reply_markup=markup
        )

    # ✅ تأكيد المهمة
    @bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
    def confirm_task(call):
        user_id = call.from_user.id
        task_id = int(call.data.split("_")[1])

        key = (user_id, task_id)

        if key not in user_task_time:
            bot.answer_callback_query(call.id, "❌ لم تبدأ المهمة")
            return

        start_time = user_task_time[key]
        elapsed = time.time() - start_time

        # حذف من الذاكرة
        del user_task_time[key]

        # ❌ لو غش
        if elapsed < 20:
            bot.send_message(
                call.message.chat.id,
                "❌ عدت بدري! سيتم حظر المهمة ليوم كامل"
            )

            return

        # ✅ نجاح
        conn = get_connection()
        cur = conn.cursor()

        # إضافة النقاط
        cur.execute("""
        UPDATE users
        SET balance = balance + (
            SELECT reward FROM tasks WHERE id=%s
        )
        WHERE user_id=%s
        """, (task_id, user_id))

        conn.commit()
        cur.close()
        conn.close()

        bot.send_message(
            call.message.chat.id,
            "✅ تم تنفيذ المهمة بنجاح 💰"
        )
