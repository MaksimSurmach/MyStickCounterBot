import telebot

from mystickcounterbot.models.messages import Messages, KeyboardButtons


def init_actions(bot: telebot.TeleBot):
    # remove menu
    bot.register_message_handler(commands=["stats"], callback=show_stat_menu, pass_bot=True)
    bot.register_message_handler(func=lambda message: message.text == KeyboardButtons.STATS.value,
                                 callback=show_stat_menu, pass_bot=True)


def show_stat_menu(message, bot):
    bot.send_message(message.chat.id, Messages.TBD.value, parse_mode="Markdown")

