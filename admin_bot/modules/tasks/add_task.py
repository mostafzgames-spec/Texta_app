@bot.message_handler(commands=['start'])
def start_admin(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ انت مش ادمن")
        return

    bot.send_message(
        message.chat.id,
        "👑 مرحبا بك في بوت الادمن\n\n"
        "📌 الأوامر:\n"
        "/addtask - إضافة مهمة"
    )
