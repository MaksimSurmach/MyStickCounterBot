from . import actions, add, remove, goal


def init_telegram_commands(bot):
    actions.init_actions(bot)
    add.init_actions(bot)
    remove.init_actions(bot)
    goal.init_actions(bot)