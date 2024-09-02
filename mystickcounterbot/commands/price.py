import telebot

from mystickcounterbot.models.messages import Messages, KeyboardButtons


def init_actions(bot: telebot.TeleBot):
    bot.register_message_handler(commands=["setprice"], callback=show_price_menu, pass_bot=True)
    bot.register_message_handler(func=lambda message: message.text == KeyboardButtons.STATS.value,
                                 callback=show_price_menu, pass_bot=True)


def show_price_menu(message, bot):
    bot.send_message(message.chat.id, Messages.TBD.value, parse_mode="Markdown")

