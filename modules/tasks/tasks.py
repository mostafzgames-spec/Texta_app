from database import get_connection
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

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
            bot.send_message(message.chat.id, "❌ لا توجد إعلانات حالياً")
            return

        # عرض كل إعلان لوحده
        for i, task in enumerate(tasks, start=1):
            task_id, title, reward = task

            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton(
                    "🎯 استلام الإعلان",
                    callback_data=f"task_{task_id}"
                )
            )

            bot.send_message(
                message.chat.id,
                f"📢 إعلان {i} | 💰 {reward} نقطة\n"
                f"📌 {title}",
                reply_markup=markup
            )

    # ▶️ عند الضغط على استلام الإعلان
    @bot.callback_query_handler(func=lambda call: call.data.startswith("task_"))
    def open_task(call):
        task_id = int(call.data.split("_")[1])

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT title, description, link, reward FROM tasks WHERE id=%s", (task_id,))
        task = cur.fetchone()

        cur.close()
        conn.close()

        if not task:
            bot.answer_callback_query(call.id, "❌ الإعلان غير موجود")
            return

        title, desc, link, reward = task

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔗 فتح الإعلان", url=link))

        bot.send_message(
            call.message.chat.id,
            f"📢 {title}\n\n"
            f"📝 {desc}\n\n"
            f"💰 {reward} نقطة",
            reply_markup=markup
        )
