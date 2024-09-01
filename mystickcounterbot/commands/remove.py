import json

import telebot

from mystickcounterbot.models.callback import get_callback_type, ReduceQuery
from mystickcounterbot.models.data import StickActivityMetadata
from mystickcounterbot.models.messages import Messages, KeyboardButtons


def init_actions(bot: telebot.TeleBot):
    # remove menu
    bot.register_message_handler(commands=["remove"], callback=show_remove_menu, pass_bot=True)
    bot.register_message_handler(func=lambda message: message.text == KeyboardButtons.REMOVE_STICK.value,
                                 callback=show_remove_menu, pass_bot=True)

    # remove value
    bot.register_callback_query_handler(func=lambda call: get_callback_type(call.data) == ReduceQuery(number=1).type,
                                        callback=remove_stick_query, pass_bot=True)


def show_remove_menu(message, bot):
    if message.text.startswith("/remove") and len(message.text.split()) > 1:
        try:
            count = int(message.text.split()[1])
            remove_stick_command(message, bot, count)
            return
        except ValueError:
            pass
    bot.send_message(message.chat.id, Messages.REMOVE_STICK_MENU.value, reply_markup=numpad_keyboard(),
                     parse_mode="Markdown")


def remove_stick_query(call, bot):
    stick_data = StickActivityMetadata(**json.loads(call.data), user_id=call.message.chat.id)
    if remove_stick_value(stick_data, bot) is False:
        bot.answer_callback_query(call.id, text=Messages.ERROR.value)
    else:
        bot.answer_callback_query(call.id, text=f"Removed {stick_data.count} sticks")


def remove_stick_command(message, bot, count: int):
    stick_data = StickActivityMetadata(number=count, user_id=message.chat.id)
    remove_stick_value(stick_data, bot)


def remove_stick_value(data: StickActivityMetadata, bot):
    bot.logging.info(f"Scheduled to remove {data.count} sticks for user {data.user_id}")
    if bot.db.remove_last_cigarette(data.dict(), data.count) is False:
        bot.logging.error(f"Failed to delete from database for user {data.user_id}")
        bot.send_message(data.user_id, Messages.ERROR.value)
        return False

    bot.send_message(data.user_id, f"Removed {data.count} sticks")
    bot.logging.info(f"Removed {data.count} sticks for user {data.user_id}")
    return True


def numpad_keyboard():
    def create_buttons(start: int = 1, end: int = 10):
        buttons = []
        for i in range(start, end + 1):
            buttons.append(telebot.types.InlineKeyboardButton(text=str(i), callback_data=ReduceQuery(number=i).json()))
        return buttons

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
    # first wide row
    keyboard.row(telebot.types.InlineKeyboardButton(text="1", callback_data=ReduceQuery(number=1).json()))
    # second row with other buttons
    keyboard.row(*create_buttons(2, 5))

    return keyboard
