from . import actions, add, remove, goal, stats, price


def init_telegram_commands(bot):
    actions.init_actions(bot)
    add.init_actions(bot)
    remove.init_actions(bot)
    goal.init_actions(bot)
    stats.init_actions(bot)
    price.init_actions(bot)