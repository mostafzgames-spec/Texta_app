from database import get_connection

def register_start(bot):

    @bot.message_handler(commands=['start'])
    def start(message):
        user_id = message.from_user.id

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        user = cur.fetchone()

        if not user:
            cur.execute("INSERT INTO users (user_id) VALUES (%s)", (user_id,))
            conn.commit()

        cur.close()
        conn.close()

        bot.send_message(message.chat.id, "👋 أهلا بك في البوت")
