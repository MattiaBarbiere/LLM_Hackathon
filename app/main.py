#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.


Usage:

```python
python echobot.py
```

Press Ctrl-C on the command line to stop the bot.

"""

import logging
import os

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from handlers.msg_handler import msg_handler_text
from handlers.qa_state import qa_text
from keys import TELEGRAM_KEY

# Our imports
from utils.utils import delete_temp_saving
from handlers.input_state import input_image, input_text, input_audio
from game_state import GameState

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Constants for the bot
DELETE_PHOTOS = True


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    print(context)
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    print(update.message.text)
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_KEY).build()

    # Add our state object to the application so that we can access it in the handlers
    application.bot_data["game_state"] = GameState()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, input_image, block=True))

    # If the input is a text, we will handle it in the input state
    application.add_handler(MessageHandler(filters.TEXT  & ~filters.COMMAND, input_text, block=True))

    # If the input is an audio, we will handle it in the input state
    application.add_handler(MessageHandler(filters.VOICE & ~filters.COMMAND, input_audio, block=True))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

    # Print the inputs attribute of the GameState object
    print("Inputs: ", application.bot_data["game_state"].inputs)

    # Delete all the files saved in the saved_photos folder
    if DELETE_PHOTOS:
        delete_temp_saving()


if __name__ == "__main__":
    main()
