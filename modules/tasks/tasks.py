from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from .tasks_db import get_tasks, get_task

def register_tasks(bot):

    @bot.message_handler(func=lambda msg: msg.text == "مهام")
    def tasks(message):
        tasks = get_tasks()

        for t in tasks:
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton(
                    "ابدأ المهمة",
                    callback_data=f"task_{t[0]}"
                )
            )

            bot.send_message(
                message.chat.id,
                f"📌 {t[1]}\n💰 {t[2]} نقطة",
                reply_markup=markup
            )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("task_"))
    def start_task(call):
        task_id = int(call.data.split("_")[1])
        task = get_task(task_id)

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("فتح الإعلان", url=task[3]))

        bot.send_message(
            call.message.chat.id,
            f"{task[1]}\n\n{task[2]}\n💰 {task[4]} نقطة",
            reply_markup=markup
        )
