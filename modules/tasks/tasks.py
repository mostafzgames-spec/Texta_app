from database import get_connection
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

def register_tasks(bot):

    print("✅ register_tasks اشتغل")

    @bot.message_handler(func=lambda msg: msg.text and msg.text.strip() == "المهام")
    def show_tasks(message):
        print("🔥 المستخدم ضغط المهام")

        user_id = message.from_user.id
        today = datetime.now().date()

        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
            SELECT id, title, reward FROM tasks
            WHERE id NOT IN (
                SELECT task_id FROM user_tasks
                WHERE user_id=%s AND date=%s
            )
            """, (user_id, today))

            tasks = cur.fetchall()

        except Exception as e:
            print("❌ خطأ في الداتابيز:", e)
            bot.send_message(message.chat.id, "❌ في مشكلة في السيرفر")
            return

        finally:
            cur.close()
            conn.close()

        if not tasks:
            bot.send_message(message.chat.id, "📭 لا توجد مهام حالياً")
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
                f"📢 مهمة {i} | 💰 {reward} نقطة\n📌 {title}",
                reply_markup=markup
            )
