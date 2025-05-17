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
from utils.image_utils import delete_saved_photos
from handlers.input_state import input_image, input_text
from game_state import GameState
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

    # Add our state object to the application so that we can access it in the handlers
    application.bot_data["game_state"] = GameState()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("image", generate_image_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, input_image, block=True))

    # If the input is a text, we will handle it in the input state
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg_handler_text, block=True))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

    # Print the inputs attribute of the GameState object
    print("Inputs: ", application.bot_data["game_state"].inputs)

    # Delete all the files saved in the saved_photos folder
    if DELETE_PHOTOS:
        delete_saved_photos()


if __name__ == "__main__":
    main()
