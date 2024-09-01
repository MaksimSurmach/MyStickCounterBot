from config import Config

import logging
import telebot

from mystickcounterbot.commands import init_telegram_commands
from mystickcounterbot.databases.mongo import MongoDB


def setup_logging():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )


def main():
    setup_logging()
    config = Config()
    db = MongoDB(config.db.uri, config.db.db_name, config.db.username, config.db.password.get_secret_value())
    db.connect()
    db.init_db()

    bot = telebot.TeleBot(config.telegram.token.get_secret_value())
    bot.db = db
    bot.logging = logging

    init_telegram_commands(bot)

    logging.info("Start telegram bot")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
