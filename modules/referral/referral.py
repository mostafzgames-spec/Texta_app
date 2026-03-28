def register_referral(bot):

    @bot.message_handler(func=lambda msg: msg.text == "دعوة أصدقاء")
    def ref(message):
        user_id = message.from_user.id
        link = f"https://t.me/YOUR_BOT?start={user_id}"

        bot.send_message(
            message.chat.id,
            f"رابطك:\n{link}"
        )
