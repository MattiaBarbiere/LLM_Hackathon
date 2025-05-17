import logging
from telegram import Update
from telegram.ext import ContextTypes
from PIL import Image
import numpy as np
import requests
from keys import HUGGING_FACE_KEY
import time


API_URL = "https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3"
headers = {
    "Authorization": f"Bearer {HUGGING_FACE_KEY}",
}

# Our imports
from utils.LLM_utils import llm_objects_from_text


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
    # Get the text from the update
    input_text = update.message.text

    # Get the objects from the text using the LLM
    text = llm_objects_from_text(input_text)

    print(f"Text: {text}")
    
    # Save the text to the inputs list in the game state
    context.bot_data["game_state"].inputs.extend(text)

    # respond text
    await update.message.reply_text(f"Text received: {input_text}")

async def input_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the case when the state in INPUT and we receive an audio.
    """
    # Get the audio from the update
    audio_file = await update.message.audio[-1].get_file()

    

    # respond audio
    await update.message.reply_audio(tmp_audio, caption="Audio received")