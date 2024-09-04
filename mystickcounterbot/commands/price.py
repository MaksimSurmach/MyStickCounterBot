import telebot

from mystickcounterbot.models.messages import Messages, KeyboardButtons
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.storage import StateMemoryStorage


class PriceState(StatesGroup):
    price = State()


state_storage = StateMemoryStorage()


def init_actions(bot: telebot.TeleBot):
    bot.register_message_handler(commands=["setprice"], callback=show_price_menu, pass_bot=True, pass_state=True)
    bot.register_message_handler(func=lambda message: message.text == KeyboardButtons.PRICE.value,
                                 callback=show_price_menu, pass_bot=True, pass_state=True)
    bot.register_message_handler(state=PriceState.price, isdigit=True,
                                 callback=set_price_chat, pass_bot=True, pass_state=True)


def set_price_chat(message, bot, state: StateContext):
    price = float(message.text)
    state.delete()
    set_price_value(message, bot, price)


def show_price_menu(message, bot):
    bot.logging.info(f"Price state: {bot.get_state(message.chat.id)}")
    if message.text.startswith("/setprice") and len(message.text.split()) > 1:
        try:
            price = float(message.text.split()[1])
            set_price_value(message, bot, price)
            return
        except ValueError:
            bot.send_message(message.chat.id, Messages.ERROR.value)
            return
    last_price = bot.db.get_user_price(message.chat.id)
    if last_price is not None:
        bot.send_message(message.chat.id, f"Your last price was {last_price}\n{Messages.SET_PRICE.value}",
                         parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, Messages.SET_PRICE.value, parse_mode="Markdown")
    bot.set_state(message.chat.id, PriceState.price)


def set_price_value(message, bot, price: float):
    if bot.db.set_user_price(user_id=message.chat.id, price=price) is False:
        bot.logging.error(f"Failed to set price for user {message.chat.id}")
        bot.send_message(message.chat.id, Messages.ERROR.value)
    else:
        bot.logging.info(f"Price set to {price} for user {message.chat.id}")
        bot.send_message(message.chat.id, f"Price set to {price}")
