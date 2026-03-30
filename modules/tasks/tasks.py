from database import get_connection
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import time

# ⏱️ حفظ وقت بداية المهمة
user_task_time = {}

def register_tasks(bot):

    print("✅ register_tasks اشتغل")

    # 📌 عرض المهام
    @bot.message_handler(func=lambda msg: msg.text and msg.text.strip() == "المهام")
    def show_tasks(message):
        print("🔥 المستخدم ضغط المهام")

        user_id = message.from_user.id
        today = datetime.now().date()

        conn = get_connection()
        cur = conn.cursor()

        try:
            # ❗ مؤقتًا بنجيب كل المهام عشان نشوف المشكلة
            cur.execute("""
            SELECT id, title, reward FROM tasks
            """)
            tasks = cur.fetchall()

        except Exception as e:
            print("❌ ERROR:", e)
            bot.send_message(message.chat.id, f"❌ خطأ في الداتابيز:\n{e}")
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

    # ▶️ فتح المهمة
    @bot.callback_query_handler(func=lambda call: call.data.startswith("start_"))
    def start_task(call):
        user_id = call.from_user.id
        task_id = int(call.data.split("_")[1])

        user_task_time[(user_id, task_id)] = time.time()

        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
            SELECT title, description, link, reward 
            FROM tasks WHERE id=%s
            """, (task_id,))
            task = cur.fetchone()

        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ:\n{e}")
            return

        finally:
            cur.close()
            conn.close()

        if not task:
            bot.answer_callback_query(call.id, "❌ المهمة غير موجودة")
            return

        title, desc, link, reward = task

        if not link.startswith("http"):
            link = "https://" + link

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔗 فتح الرابط", url=link))
        markup.add(InlineKeyboardButton("✅ تأكيد المهمة", callback_data=f"confirm_{task_id}"))

        bot.send_message(
            call.message.chat.id,
            f"📢 {title}\n\n"
            f"📝 {desc}\n\n"
            f"💰 {reward} نقطة\n\n"
            f"📌 افتح الرابط وانتظر 20 ثانية ثم اضغط تأكيد",
            reply_markup=markup
        )

    # ✅ تأكيد المهمة
    @bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
    def confirm_task(call):
        user_id = call.from_user.id
        task_id = int(call.data.split("_")[1])

        key = (user_id, task_id)

        if key not in user_task_time:
            bot.answer_callback_query(call.id, "❌ ابدأ المهمة الأول")
            return

        elapsed = time.time() - user_task_time[key]
        del user_task_time[key]

        conn = get_connection()
        cur = conn.cursor()

        today = datetime.now().date()

        try:
            # تسجيل إن المستخدم عمل المهمة
            cur.execute("""
            INSERT INTO user_tasks (user_id, task_id, date)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
            """, (user_id, task_id, today))

            # ❌ لو أقل من 20 ثانية
            if elapsed < 20:
                conn.commit()
                bot.send_message(call.message.chat.id, "⏱️ حاول تستنى شوية قبل التأكيد 😉")
                return

            # ✅ إضافة النقاط
            cur.execute("""
            UPDATE users
            SET balance = balance + (
                SELECT reward FROM tasks WHERE id=%s
            )
            WHERE user_id=%s
            """, (task_id, user_id))

            conn.commit()

        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ:\n{e}")
            return

        finally:
            cur.close()
            conn.close()

        bot.send_message(call.message.chat.id, "✅ تم إضافة النقاط بنجاح 💰")
