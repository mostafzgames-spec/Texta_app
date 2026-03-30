import time
from datetime import date
from database import get_connection
import telebot

user_task_time = {}
user_task_message = {}

# ================= عرض المهام =================
def show_tasks(bot, msg):
    user_id = msg.from_user.id

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM tasks WHERE id NOT IN (
            SELECT task_id FROM user_tasks
            WHERE user_id = %s AND date = %s
        )
    """, (user_id, date.today()))

    tasks = cur.fetchall()

    if not tasks:
        bot.send_message(msg.chat.id, "❌ لا توجد مهام اليوم")
        return

    for task in tasks:
        task_id, name, desc, link, reward = task

        text = f"""
📢 مهمة {task_id}
💰 {reward} نقطة
📌 {name}
"""

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            telebot.types.InlineKeyboardButton(
                "🚀 فتح المهمة",
                callback_data=f"open_{task_id}"
            )
        )

        bot.send_message(msg.chat.id, text, reply_markup=keyboard)

    cur.close()
    conn.close()


# ================= تسجيل الأحداث =================
def register_tasks(bot):

    # ---------- فتح المهمة ----------
    @bot.callback_query_handler(func=lambda call: call.data.startswith("open_"))
    def open_task(call):
        try:
            bot.answer_callback_query(call.id)  # 🔥 مهم

            task_id = int(call.data.split("_")[1])
            user_id = call.from_user.id

            user_task_time[(user_id, task_id)] = time.time()

            conn = get_connection()
            cur = conn.cursor()

            cur.execute("SELECT name, description, link, reward FROM tasks WHERE id = %s", (task_id,))
            task = cur.fetchone()

            if not task:
                bot.send_message(call.message.chat.id, "❌ المهمة غير موجودة")
                return

            name, desc, link, reward = task

            text = f"""
📢 {name}

📝 {desc}

💰 {reward} نقطة
"""

            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(
                telebot.types.InlineKeyboardButton("🔗 فتح الرابط", url=link)
            )
            keyboard.add(
                telebot.types.InlineKeyboardButton("✅ تأكيد المهمة", callback_data=f"confirm_{task_id}")
            )

            msg = bot.send_message(call.message.chat.id, text, reply_markup=keyboard)

            user_task_message[(user_id, task_id)] = msg.message_id

            cur.close()
            conn.close()

        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ:\n{e}")


    # ---------- تأكيد المهمة ----------
    @bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
    def confirm_task(call):
        try:
            bot.answer_callback_query(call.id)  # 🔥 مهم

            user_id = call.from_user.id
            task_id = int(call.data.split("_")[1])

            key = (user_id, task_id)

            if key not in user_task_time:
                bot.send_message(call.message.chat.id, "❌ افتح المهمة الأول")
                return

            diff = time.time() - user_task_time[key]

            conn = get_connection()
            cur = conn.cursor()

            chat_id = call.message.chat.id

            # 🧹 حذف رسالة المهمة
            if key in user_task_message:
                try:
                    bot.delete_message(chat_id, user_task_message[key])
                except:
                    pass

            # ❌ رجع بدري
            if diff < 20:
                bot.send_message(chat_id, "❌ رجعت بدري! تم إلغاء المهمة")

                cur.execute("""
                    INSERT INTO user_tasks (user_id, task_id, date)
                    VALUES (%s, %s, %s)
                """, (user_id, task_id, date.today()))

                conn.commit()
                cur.close()
                conn.close()

                # 🔥 رجوع للقائمة
                show_tasks(bot, call.message)
                return

            # ✅ نجح
            cur.execute("SELECT reward FROM tasks WHERE id = %s", (task_id,))
            result = cur.fetchone()

            if not result:
                bot.send_message(chat_id, "❌ المهمة غير موجودة")
                return

            reward = result[0]

            cur.execute("""
                UPDATE users 
                SET points = COALESCE(points,0) + %s 
                WHERE user_id = %s
            """, (reward, user_id))

            cur.execute("""
                INSERT INTO user_tasks (user_id, task_id, date)
                VALUES (%s, %s, %s)
            """, (user_id, task_id, date.today()))

            conn.commit()
            cur.close()
            conn.close()

            bot.send_message(chat_id, "✅ تم إضافة النقاط بنجاح 💰")

            # 🔥 رجوع للقائمة
            show_tasks(bot, call.message)

        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ:\n{e}")
