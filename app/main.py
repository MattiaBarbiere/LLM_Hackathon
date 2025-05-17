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

from handlers.idle_state import idle_text
from handlers.qa_state import qa_text
from handlers.state_handler import StateHandlerFactory
from keys import TELEGRAM_KEY

# Our imports
from utils.utils import delete_temp_saving
from game_state import GameState, State
from handlers.input_state import input_image, input_text, input_audio
from utils.utils import delete_temp_saving
from utils.query import generate_image

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


async def generate_image_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /image command"""
    # Extract prompt from command arguments
    if not context.args:
        await update.message.reply_text(
            "Please provide a description for the image. Example: /image a beautiful sunset")
        return

    prompt = " ".join(context.args)
    user_id = update.message.from_user.id

    # Send a "generating" message first to show the bot is working
    message = await update.message.reply_text(f"Generating image of: {prompt}...")

    # Call image generation function
    success, result = generate_image(prompt, user_id)

    if success:
        try:
            # Download the image
            import requests
            from io import BytesIO

            image_response = requests.get(result)
            image_data = BytesIO(image_response.content)

            # Send the image
            await update.message.reply_photo(
                photo=image_data,
                caption=f"Generated image for: \"{prompt}\"\nModel: FLUX.1-schnell"
            )

            # Delete the "generating" message
            await message.delete()
        except Exception as e:
            await message.edit_text(f"Error downloading image: {str(e)}")
    else:
        # If image generation failed, update the message with the error
        await message.edit_text(result)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_KEY).build()

    # Add our state object to the application
    application.bot_data["game_state"] = GameState()

    # Create state handler factory
    state_handler = StateHandlerFactory(application)
    application.bot_data["state_handler"] = state_handler

    # Register command handlers (these are global and not state-dependent)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("image", generate_image_command))

    # Register state-specific handlers
    # IDLE state
    state_handler.register_handler(State.IDLE, filters.TEXT & ~filters.COMMAND, idle_text)

    # INPUT state
    state_handler.register_handler(State.INPUT, filters.TEXT & ~filters.COMMAND, input_text)
    state_handler.register_handler(State.INPUT, filters.PHOTO & ~filters.COMMAND, input_image)
    state_handler.register_handler(State.INPUT, filters.VOICE & ~filters.COMMAND, input_audio)

    # QA state
    state_handler.register_handler(State.QA, filters.TEXT & ~filters.COMMAND, qa_text)

    # Initialize with the starting state (IDLE)
    state_handler.update_handlers(State.IDLE)

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

    # Print the inputs attribute of the GameState object
    print("Inputs: ", application.bot_data["game_state"].inputs)

    # Delete all the files saved in the saved_photos folder
    if DELETE_PHOTOS:
        delete_temp_saving()


if __name__ == "__main__":
    main()
