import time
from datetime import date
from database import get_connection
import telebot

user_task_time = {}

def show_tasks(bot, msg):
    user_id = msg.from_user.id

    conn = get_connection()
    cur = conn.cursor()

    # نجيب المهام اللي المستخدم معملهاش النهارده
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


def register_tasks(bot):

    @bot.callback_query_handler(func=lambda call: call.data.startswith("open_"))
    def open_task(call):
        task_id = int(call.data.split("_")[1])
        user_id = call.from_user.id

        user_task_time[(user_id, task_id)] = time.time()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT link FROM tasks WHERE id = %s", (task_id,))
        link = cur.fetchone()[0]

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            telebot.types.InlineKeyboardButton("🔗 فتح الرابط", url=link)
        )
        keyboard.add(
            telebot.types.InlineKeyboardButton("✅ تأكيد المهمة", callback_data=f"confirm_{task_id}")
        )

        bot.send_message(call.message.chat.id,
            "📌 افتح الرابط واستنى شوية قبل التأكيد 😉",
            reply_markup=keyboard
        )

        cur.close()
        conn.close()


    @bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
    def confirm_task(call):
        user_id = call.from_user.id
        task_id = int(call.data.split("_")[1])

        key = (user_id, task_id)

        if key not in user_task_time:
            bot.answer_callback_query(call.id, "❌ افتح المهمة الأول")
            return

        diff = time.time() - user_task_time[key]

        conn = get_connection()
        cur = conn.cursor()

        # ❌ رجع بدري
        if diff < 20:
            bot.send_message(call.message.chat.id, "❌ رجعت بدري! تم إلغاء المهمة")

            cur.execute("""
                INSERT INTO user_tasks (user_id, task_id, date)
                VALUES (%s, %s, %s)
            """, (user_id, task_id, date.today()))

            conn.commit()
            cur.close()
            conn.close()
            return

        # ✅ نجح
        cur.execute("SELECT reward FROM tasks WHERE id = %s", (task_id,))
        reward = cur.fetchone()[0]

        cur.execute("UPDATE users SET points = points + %s WHERE user_id = %s",
                    (reward, user_id))

        cur.execute("""
            INSERT INTO user_tasks (user_id, task_id, date)
            VALUES (%s, %s, %s)
        """, (user_id, task_id, date.today()))

        conn.commit()
        cur.close()
        conn.close()

        bot.send_message(call.message.chat.id, "✅ تم إضافة النقاط بنجاح 💰")
