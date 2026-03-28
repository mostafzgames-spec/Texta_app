from database import get_connection
from admin_bot.config import ADMIN_ID

data = {}

def register_add_task(bot):

    @bot.message_handler(commands=['addtask'])
    def add(message):
        if message.from_user.id != ADMIN_ID:
            return

        data[message.from_user.id] = {}
        bot.send_message(message.chat.id, "اسم المهمة:")

    @bot.message_handler(func=lambda m: m.from_user.id in data)
    def steps(message):
        uid = message.from_user.id

        if "title" not in data[uid]:
            data[uid]["title"] = message.text
            bot.send_message(message.chat.id, "الوصف:")
        elif "description" not in data[uid]:
            data[uid]["description"] = message.text
            bot.send_message(message.chat.id, "الرابط:")
        elif "link" not in data[uid]:
            data[uid]["link"] = message.text
            bot.send_message(message.chat.id, "النقاط:")
        else:
            data[uid]["reward"] = int(message.text)

            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
            INSERT INTO tasks (title, description, link, reward)
            VALUES (%s, %s, %s, %s)
            """, (
                data[uid]["title"],
                data[uid]["description"],
                data[uid]["link"],
                data[uid]["reward"]
            ))

            conn.commit()
            cur.close()
            conn.close()

            bot.send_message(message.chat.id, "✅ تمت الإضافة")
            del data[uid]
