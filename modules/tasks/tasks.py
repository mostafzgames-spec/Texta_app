from database import get_connection
import time

last_click = {}

def register_tasks(bot):

    # عرض المهام
    @bot.message_handler(commands=['tasks'])
    def show_tasks(message):
        user_id = message.from_user.id

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, title, description, link, reward FROM tasks")
        tasks = cur.fetchall()

        cur.close()
        conn.close()

        if not tasks:
            bot.send_message(message.chat.id, "❌ لا توجد مهام حالياً")
            return

        for task in tasks:
            task_id, title, desc, link, reward = task

            bot.send_message(
                message.chat.id,
                f"📌 {title}\n\n"
                f"{desc}\n\n"
                f"🔗 {link}\n"
                f"💰 {reward} نقطة\n\n"
                f"اضغط:\n/starttask_{task_id}"
            )

    # بدء المهمة
    @bot.message_handler(func=lambda m: m.text.startswith("/starttask_"))
    def start_task(message):
        user_id = message.from_user.id
        task_id = int(message.text.split("_")[1])

        now = time.time()

        # ⛔ منع تنفيذ مهمة كل 3 دقائق
        if user_id in last_click:
            if now - last_click[user_id] < 180:
                bot.send_message(message.chat.id, "⏳ استنى 3 دقائق بين كل مهمة")
                return

        last_click[user_id] = now

        conn = get_connection()
        cur = conn.cursor()

        # منع التكرار
        cur.execute("""
        SELECT * FROM user_tasks
        WHERE user_id = %s AND task_id = %s
        """, (user_id, task_id))

        if cur.fetchone():
            bot.send_message(message.chat.id, "❌ نفذت المهمة قبل كده")
            cur.close()
            conn.close()
            return

        # جلب النقاط
        cur.execute("SELECT reward FROM tasks WHERE id = %s", (task_id,))
        reward = cur.fetchone()[0]

        # تسجيل التنفيذ
        cur.execute("""
        INSERT INTO user_tasks (user_id, task_id, last_done)
        VALUES (%s, %s, NOW())
        """, (user_id, task_id))

# إضافة نقاط
cur.execute("""
UPDATE users
SET balance = balance + %s
WHERE user_id = %s
""", (reward, user_id))

conn.commit()
cur.close()
conn.close()

bot.send_message(
    message.chat.id,
    f"✅ تم تنفيذ المهمة\n💰 +{reward} نقطة"
)
