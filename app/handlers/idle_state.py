from telegram import Update
from telegram.ext import ContextTypes
from game_state import State
from utils.transitions import transition_state


async def idle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages in IDLE state"""
    message = update.message.text
    user_id = update.message.from_user.id

    # Process message in IDLE state
    if message.lower() == "start game" or message.lower() == "play":
        # User wants to start the game, transition to INPUT state
        await transition_state(
            update,
            context,
            State.INPUT,
            message="Game started! I'm ready to receive your input."
        )
    elif message.lower() == "help":
        await update.message.reply_text("Type 'start game' or 'play' to begin playing.")
    else:
        await update.message.reply_text("Welcome! Type 'start game' to begin or 'help' for instructions.")
