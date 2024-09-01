import telebot

from mystickcounterbot.models.callback import AddMenuQuery, ReduceMenuQuery
from mystickcounterbot.models.data import UserMetaData
from mystickcounterbot.models.messages import KeyboardButtons, Messages


def init_actions(bot: telebot.TeleBot):
    @bot.message_handler(commands=["start"])
    def start_command(message):
        sync_user_data(message, bot)
        bot.send_message(message.chat.id, Messages.START.value, reply_markup=keyboard_menu(), parse_mode="Markdown")

    @bot.message_handler(commands=["help"])
    def help_command(message):
        sync_user_data(message, bot)
        bot.send_message(message.chat.id, Messages.HELP.value, reply_markup=keyboard_menu(), parse_mode="Markdown")

    bot.register_callback_query_handler(func=lambda call: call.data == AddMenuQuery().json(),
                                        callback=add_menu, pass_bot=True)


def sync_user_data(message, bot):
    if bot.db.get_user(message.chat.id) is None:
        usr_metadata = UserMetaData(user_id=message.chat.id, username=message.chat.username)
        if bot.db.create_user(usr_metadata.dict()) is False:
            bot.logging.error(f"Failed to create user {message.chat.id}")
        else:
            bot.logging.info(f"User {message.chat.id} created")




def add_menu(call, bot):
    bot.send_message(call.message.chat.id, "How many sticks do you want to add?")
    bot.answer_callback_query(call.id)


def homepage_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="Add smoked stick", callback_data=AddMenuQuery().json()))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Reduce smoked stick", callback_data=ReduceMenuQuery().json()))
    return keyboard


def keyboard_menu():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButtons.ADD_ONE_STICK.value)
    keyboard.row(KeyboardButtons.ADD_STICK.value, KeyboardButtons.REMOVE_STICK.value)
    keyboard.row(KeyboardButtons.GOAL.value, KeyboardButtons.PRICE.value, KeyboardButtons.STATS.value)
    keyboard.row(KeyboardButtons.HELP.value)
    return keyboard
