from telegram import Update
from telegram.ext import ContextTypes
from utils.transitions import transition_state
from game_state import State
import random


async def check_input_length(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Check the length of the input text and respond accordingly.
    """
    if len(context.bot_data["game_state"].inputs) >= context.bot_data["game_state"].number_of_inputs:
        # Randomly choose an object from the inputs
        obj = random.choice(context.bot_data["game_state"].inputs)
        print(f"Chosen object: {obj}")
        context.bot_data["game_state"].secret_word = obj
        await transition_state(
            update,
            context,
            State.QA,
            message=f"Got: {context.bot_data["game_state"].inputs}\nEnough inputs, now to the Q&A State!"
        )
    else:
        await update.message.reply_text(
            f"You have this set of objects: {context.bot_data['game_state'].inputs}\n"
            f"Please provide {context.bot_data['game_state'].number_of_inputs - len(context.bot_data['game_state'].inputs)} more objects."
        )
