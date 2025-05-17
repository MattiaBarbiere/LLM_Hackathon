import logging

from telegram import Update
from telegram.ext import ContextTypes
from PIL import Image
import numpy as np

# Handle for the input state of the app if the input is an image
async def input_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the case when the state in INPUT and we receive an image.
    """
    
    photo_file = await update.message.photo[-1].get_file()

    # load image into numpy array
    tmp_photo = "app/saved_photos/tmp_photo.jpg"
    await photo_file.download_to_drive(tmp_photo)
    img = np.array(Image.open(tmp_photo))

    # To object detection
    # ...

    # Save the objects to the inputs list in the game state
    context.bot_data["game_state"].inputs.append("Hello world")

    # respond photo
    await update.message.reply_photo(tmp_photo, caption=f"Image shape: {img.shape}")

async def input_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the case when the state in INPUT and we receive a text.
    """
    # Separate the text by commas
    text = update.message.text.split(",")
    
    # Save the text to the inputs list in the game state
    context.bot_data["game_state"].inputs.extend(text)

    # respond text
    await update.message.reply_text(f"Text received: {update.message.text}")