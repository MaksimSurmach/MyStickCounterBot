import json

import telebot

from mystickcounterbot.models.callback import AddQuery, get_callback_type
from mystickcounterbot.models.data import StickActivityMetadata, StickAddedMessageData
from mystickcounterbot.models.messages import Messages, KeyboardButtons


def init_actions(bot: telebot.TeleBot):
    # Add menu
    bot.register_message_handler(commands=["add"], callback=show_add_menu, pass_bot=True)
    bot.register_message_handler(func=lambda message: message.text == KeyboardButtons.ADD_STICK.value,
                                 callback=show_add_menu, pass_bot=True)

    # Add value
    bot.register_callback_query_handler(func=lambda call: get_callback_type(call.data) == AddQuery(number=1).type,
                                        callback=add_StickActivity_query, pass_bot=True)

    bot.register_message_handler(func=lambda message: message.text == KeyboardButtons.ADD_ONE_STICK.value,
                                 callback=add_StickActivity_menu, pass_bot=True)


def show_add_menu(message, bot):
    if message.text.startswith("/add") and len(message.text.split()) > 1:
        try:
            count = int(message.text.split()[1])
            add_StickActivity_command(message, bot, count)
            return
        except ValueError:
            pass
    bot.send_message(message.chat.id, Messages.ADD_STICK_MENU.value, reply_markup=numpad_keyboard(),
                     parse_mode="Markdown")


def add_StickActivity_query(call, bot):
    stick_data = StickActivityMetadata(**json.loads(call.data), user_id=call.message.chat.id)
    if add_StickActivity_value(stick_data, bot) is False:
        bot.answer_callback_query(call.id, text=Messages.ERROR)
    else:
        bot.answer_callback_query(call.id, text=f"Added {stick_data.count} sticks")


def add_StickActivity_menu(message, bot):
    stick_data = StickActivityMetadata(number=1, user_id=message.chat.id)
    add_StickActivity_value(stick_data, bot)


def add_StickActivity_command(message, bot, count: int):
    stick_data = StickActivityMetadata(number=count, user_id=message.chat.id)
    add_StickActivity_value(stick_data, bot)


def add_StickActivity_value(data: StickActivityMetadata, bot):
    last_smoked = bot.db.get_last_cigarette_time(data.user_id)  # get last smoked time
    if bot.db.add_stick(data.dict()) is False:
        bot.send_message(data.user_id, Messages.ERROR)
        return False

    today_smoked = bot.db.get_total_cigarettes_today(data.user_id)
    user_goal = bot.db.get_user_goal(data.user_id)
    message_data = StickAddedMessageData(today_smoked=int(today_smoked),
                                         added_stick=int(data.count))
    message_data.goal.daily_goal = user_goal
    if last_smoked:
        message_data.last_smoked = data.timestamp - last_smoked
    bot.send_message(data.user_id, Messages.stick_added(message_data), parse_mode="Markdown")
    return True


def numpad_keyboard():
    def create_buttons(start: int = 1, end: int = 10):
        buttons = []
        for i in range(start, end + 1):
            buttons.append(telebot.types.InlineKeyboardButton(text=str(i), callback_data=AddQuery(number=i).json()))
        return buttons

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
    # first wide row
    keyboard.row(telebot.types.InlineKeyboardButton(text="1", callback_data=AddQuery(number=1).json()))
    # second row with other buttons
    keyboard.row(*create_buttons(2, 5))

    return keyboard
