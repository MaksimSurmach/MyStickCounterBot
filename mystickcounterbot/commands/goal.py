import json

import telebot

from mystickcounterbot.models.callback import get_callback_type, SetGoalQuery
from mystickcounterbot.models.data import StickActivityMetadata, StickAddedMessageData, GoalMetadata
from mystickcounterbot.models.messages import Messages, KeyboardButtons


def init_actions(bot: telebot.TeleBot):
    # goal menu
    bot.register_message_handler(commands=["setgoal"], callback=show_goal_menu, pass_bot=True)
    bot.register_message_handler(func=lambda message: message.text == KeyboardButtons.GOAL.value,
                                 callback=show_goal_menu, pass_bot=True)

    # goal value
    bot.register_callback_query_handler(func=lambda call: get_callback_type(call.data) == SetGoalQuery(number=1).type,
                                        callback=set_goal_query, pass_bot=True)


def show_goal_menu(message, bot):
    if message.text.startswith("/setgoal") and len(message.text.split()) > 1:
        try:
            count = int(message.text.split()[1])
            add_StickActivity_command(message, bot, count)
            return
        except ValueError:
            pass
    bot.send_message(message.chat.id, Messages.SET_GOAL.value, reply_markup=numpad_keyboard(),
                     parse_mode="Markdown")


def set_goal_query(call, bot):
    goal_data = GoalMetadata(**json.loads(call.data), user_id=call.message.chat.id)
    if set_goal_value(goal_data, bot) is False:
        bot.answer_callback_query(call.id, text=Messages.ERROR)
    else:
        bot.answer_callback_query(call.id, text=f"Daily goal set to {goal_data.daily_goal}")


def set_goal_command(message, bot, count: int):
    stick_data = GoalMetadata(number=count, user_id=message.chat.id)
    set_goal_value(stick_data, bot)


def set_goal_value(data: GoalMetadata, bot):
    if bot.db.set_user_goal(user_id=data.user_id, goal=data.daily_goal) is False:
        bot.logging.error(f"Failed to set goal for user {data.user_id}")
        return False

    bot.send_message(data.user_id, f"Daily goal set to {data.daily_goal}")
    return True


def numpad_keyboard():
    buttons = [1, 3, 5, 8, 10, 15, 20, 25]
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons_len = len(buttons)
    keyboard.row(*[telebot.types.InlineKeyboardButton(text=str(buttons[i]), callback_data=SetGoalQuery(number=buttons[i]).json()) for i in range(buttons_len)])

    return keyboard
