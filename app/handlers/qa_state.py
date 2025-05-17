import logging
import re

import torch
from telegram import Update
from telegram.ext import ContextTypes
from PIL import Image
import numpy as np

from game_state import State
from utils.config import *
from utils.query import *
from utils.transitions import transition_state


async def qa_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text queries in QA state"""
    query = update.message.text
    user_id = update.message.from_user.id

    # Check for commands to change state
    if query.lower() == "restart" or query.lower() == "new game":
        # Clear game state data and go back to IDLE
        context.bot_data["game_state"].inputs = {}
        await transition_state(
            update,
            context,
            State.IDLE,
            message="Game reset. Type 'start game' to begin a new session."
        )
        return

    if query.lower() == "add more input":
        # User wants to provide more input
        await transition_state(
            update,
            context,
            State.INPUT,
            message="Returning to input state. You can provide additional information."
        )
        return

    # Handle normal QA interaction
    response = query_llm(query, user_id)
    await update.message.reply_text(response)
