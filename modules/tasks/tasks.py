from telebot import types
from database import get_connection
import time

# تسجيل موديل المهام
def register_tasks(bot):

    # عرض المهام
    @bot.message_handler(func=lambda message: message.text == "المهام")
    def show_tasks(message):
        try:
            conn = get_connection()
            cur = conn.cursor()

            # مهم جدًا ❗❗
            cur.execute("SELECT id, name, reward FROM tasks")
            tasks = cur.fetchall()

            if not tasks:
                bot.send_message(message.chat.id, "لا يوجد مهام حالياً ❌")
                return

            for task in tasks:
                task_id = task[0]
                name = task[1]
                reward = task[2]

                text = f"📢 مهمة {task_id}\n💰 {reward} نقطة\n📌 {name}"

                markup = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton(
                    "فتح المهمة 🚀",
                    callback_data=f"open_task_{task_id}"
                )
                markup.add(btn)

                bot.send_message(message.chat.id, text, reply_markup=markup)

        except Exception as e:
            bot.send_message(message.chat.id, f"❌ في مشكلة في السيرفر\n{e}")

    # فتح المهمة
    @bot.callback_query_handler(func=lambda call: call.data.startswith("open_task_"))
    def open_task(call):
        try:
            task_id = int(call.data.split("_")[2])

            conn = get_connection()
            cur = conn.cursor()

            # مهم جدًا ❗❗
            cur.execute("SELECT id, name, description, link, reward FROM tasks WHERE id=%s", (task_id,))
            task = cur.fetchone()

            if not task:
                bot.answer_callback_query(call.id, "المهمة غير موجودة ❌")
                return

            task_id, name, description, link, reward = task

            text = f"""📢 {name}

📝 {description}

💰 {reward} نقطة
"""

            markup = types.InlineKeyboardMarkup()

            btn_link = types.InlineKeyboardButton("فتح الرابط 🔗", url=link)
            btn_confirm = types.InlineKeyboardButton(
                "تأكيد المهمة ✅",
                callback_data=f"confirm_{task_id}"
            )

            markup.add(btn_link)
            markup.add(btn_confirm)

            # نسجل وقت الدخول
            bot.user_data = getattr(bot, "user_data", {})
            bot.user_data[call.from_user.id] = {
                "task_id": task_id,
                "time": time.time()
            }

            bot.send_message(call.message.chat.id, text, reply_markup=markup)

        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ\n{e}")

    # تأكيد المهمة
    @bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
    def confirm_task(call):
        try:
            user_id = call.from_user.id
            task_id = int(call.data.split("_")[1])

            if not hasattr(bot, "user_data") or user_id not in bot.user_data:
                bot.answer_callback_query(call.id, "ابدأ المهمة الأول ❌")
                return

            start_time = bot.user_data[user_id]["time"]
            now = time.time()

            # لو رجع بدري
            if now - start_time < 20:
                bot.send_message(call.message.chat.id, "❌ رجعت بدري! تم إلغاء المهمة")
                return

            conn = get_connection()
            cur = conn.cursor()

            # نجيب المكافأة
            cur.execute("SELECT reward FROM tasks WHERE id=%s", (task_id,))
            reward = cur.fetchone()[0]

            # نضيف نقاط
            cur.execute("UPDATE users SET points = points + %s WHERE user_id=%s", (reward, user_id))

            conn.commit()

            bot.send_message(call.message.chat.id, f"✅ تم إضافة {reward} نقطة")

        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ\n{e}")
