from .account_db import create_user, get_user

def register_account(bot):

    @bot.message_handler(commands=['start'])
    def start(message):
        user_id = message.from_user.id
        create_user(user_id)

        bot.send_message(message.chat.id, "👋 أهلا بك")

    @bot.message_handler(func=lambda msg: msg.text == "حسابي")
    def account(message):
        user = get_user(message.from_user.id)

        bot.send_message(
            message.chat.id,
            f"🆔 ID: {user[0]}\n💰 رصيدك: {user[1]}"
        )
