from database import get_connection
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def register_tasks(bot):

    @bot.message_handler(func=lambda msg: msg.text == "مهام")
    def show_tasks(message):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, title, reward FROM tasks")
        tasks = cur.fetchall()

        cur.close()
        conn.close()

        if not tasks:
            bot.send_message(message.chat.id, "❌ لا يوجد مهام حاليا")
            return

        for task in tasks:
            task_id, title, reward = task

            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton(
                    "ابدأ المهمة",
                    callback_data=f"task_{task_id}"
                )
            )

            bot.send_message(
                message.chat.id,
                f"📌 {title}\n💰 {reward} نقطة",
                reply_markup=markup
            )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("task_"))
    def start_task(call):
        task_id = int(call.data.split("_")[1])

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT title, description, link, reward FROM tasks WHERE id=%s", (task_id,))
        task = cur.fetchone()

        if not task:
            bot.answer_callback_query(call.id, "المهمة غير موجودة")
            return

        title, desc, link, reward = task

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("فتح الإعلان", url=link))

        bot.send_message(
            call.message.chat.id,
            f"📢 {title}\n\n📝 {desc}\n\n💰 {reward} نقطة",
            reply_markup=markup
        )

        cur.close()
        conn.close()
