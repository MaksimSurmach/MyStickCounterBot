import enum

from mystickcounterbot.models.data import StickAddedMessageData


class Messages(enum.Enum):
    START = """
    **Welcome to the Quit Smoking Bot!** 🚭

    I'm here to support you on your journey to quit smoking. Here’s what I can help you with:

    1. **Track Your Cigarettes**: Easily record how many cigarettes you smoke each day.
    2. **Monitor Your Progress**: View detailed statistics on your smoking habits.
    3. **Save Money**: See how much money you’ve saved by not buying cigarettes.
    4. **Set Goals**: Define your daily smoking goals and stay on track.

    To get started, just use the buttons below or type `/help` to see a list of all available commands.

    Let's work together towards a smoke-free future! 🌟
    """

    HELP = """
    ### How to Use the Bot:

    - **Commands**: Use the following commands to interact with me:
      - `/add` - Add a cigarette to your daily count.
      - `/remove` - Remove a cigarette from your daily count.
      - `/setgoal` - Set a goal for the number of cigarettes you want to smoke in a day.
      - `/setprice` - Set the price of a cigarette pack to calculate your savings.
      - `/stats` - View your smoking statistics and savings.
      - `/help` - Get a list of all commands and their descriptions.

    - **Inline Buttons**: You can also use the inline buttons provided for quick access to common actions.
    """
    ADD_STICK_MENU = "🚬 How many sticks do you want to add? \n\n" + \
                     "Press the button below or type in command.\n" + "`/add <number>`"
    REMOVE_STICK_MENU = "🗑 How many sticks do you want to remove? \n\n" + \
                        "Press the button below or type in command.\n" + "`/remove <number>`"
    REMOVE_STICK = "🚬 latest stick removed!"
    NO_STICKS = "You haven't smoked any cigarettes today."
    SET_GOAL = "🎯 Please enter your daily smoking goal. \n\n" + \
               "Press the button below or type in command.\n" + "`/setgoal <number>`"
    SET_PRICE = "💰 Please enter the price of a cigarette pack(20 sticks). \n\n" + \
                "Press the button below or type in command.\n" + "`/setprice <number>`"
    ERROR = " Error occurred."
    TBD = "This feature is still under development. Stay tuned for updates!"

    @staticmethod
    def stick_added(data: StickAddedMessageData) -> str:
        message = (
            f"🚬 +{data.added_stick} Hits!\n\n"
            f"🔥 Total smoked today: {data.today_smoked}\n\n"
        )
        # Add goal message
        if data.goal.daily_goal > 0:
            message += f"🎯 Daily goal: {data.today_smoked}/{data.goal.daily_goal}\n\n"
        elif data.goal.daily_goal == 0:
            message += "🎯 Daily goal: Not set\n\n"

        # Add last smoked message
        if data.last_smoked:
            seconds = data.last_smoked.total_seconds()
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            message += "🕒 Last smoked:"
            if hours > 24:
                message += f" {int(hours // 24)} days"
                hours %= 24
            if hours > 0:
                message += f" {int(hours)} hours"
            if minutes == 0:
                message += " less than a minute"
            else:
                message += f" {int(minutes)} minutes"
            message += " ago\n"
        return message


class Buttons(enum.Enum):
    ADD_STICK = "🚬 Add Stick"
    REMOVE_STICK = "🗑 Remove Stick"
    GOAL = "🎯 Set Goal"
    PRICE = "💰 Set Price"
    STATS = "📊 Show Statistics"


class KeyboardButtons(enum.Enum):
    ADD_ONE_STICK = "Add 1 🚬"
    ADD_STICK = "🚬 Add Stick"
    REMOVE_STICK = "🗑 Remove Stick"
    GOAL = "🎯 Set Goal"
    PRICE = "💰 Set Price"
    STATS = "📊 Show Statistics"
    HELP = "❓ Help"
