from database import get_connection
from admin_bot.config import ADMIN_ID

def register_add_task(bot):

    data = {}

    # START
    @bot.message_handler(commands=['start'])
    def start_admin(message):
        if message.from_user.id != ADMIN_ID:
            bot.send_message(message.chat.id, "❌ انت مش ادمن")
            return

        bot.send_message(
            message.chat.id,
            "👑 اهلا بيك في بوت الادمن\n\n"
            "/addtask - اضافة مهمة"
        )

    # بدء اضافة مهمة
    @bot.message_handler(commands=['addtask'])
    def add_task_start(message):
        if message.from_user.id != ADMIN_ID:
            return

        bot.send_message(message.chat.id, "📌 اكتب اسم المهمة:")
        bot.register_next_step_handler(message, get_title)

    def get_title(message):
        data[message.chat.id] = {"title": message.text}
        bot.send_message(message.chat.id, "📝 اكتب وصف المهمة:")
        bot.register_next_step_handler(message, get_desc)

    def get_desc(message):
        data[message.chat.id]["description"] = message.text
        bot.send_message(message.chat.id, "🔗 اكتب الرابط:")
        bot.register_next_step_handler(message, get_link)

    def get_link(message):
        data[message.chat.id]["link"] = message.text
        bot.send_message(message.chat.id, "💰 اكتب النقاط:")
        bot.register_next_step_handler(message, get_reward)

    def get_reward(message):
        try:
            reward = int(message.text)
        except:
            bot.send_message(message.chat.id, "❌ لازم رقم")
            return

        task = data[message.chat.id]

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO tasks (title, description, link, reward)
        VALUES (%s, %s, %s, %s)
        """, (task["title"], task["description"], task["link"], reward))

        conn.commit()
        cur.close()
        conn.close()

        bot.send_message(message.chat.id, "✅ تم إضافة المهمة")
