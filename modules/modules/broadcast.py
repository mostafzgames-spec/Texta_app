from database import get_connection
from admin_bot.config import ADMIN_ID

def register_broadcast(bot):

    @bot.message_handler(commands=['broadcast'])
    def broadcast_start(message):
        if message.from_user.id != ADMIN_ID:
            return

        bot.send_message(message.chat.id, "📢 اكتب الرسالة:")
        bot.register_next_step_handler(message, send_broadcast)

    def send_broadcast(message):
        text = message.text

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT user_id FROM users")
        users = cur.fetchall()

        sent = 0

        for user in users:
            try:
                bot.send_message(user[0], text)
                sent += 1
            except:
                pass

        cur.close()
        conn.close()

        bot.send_message(message.chat.id, f"✅ تم الإرسال لـ {sent} مستخدم")
