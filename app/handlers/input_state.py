import logging
from telegram import Update
from telegram.ext import ContextTypes

from game_state import State
# Our imports
from utils.LLM_utils import llm_objects_from_text
from utils.audio_utils import audio_to_text
from utils.query import choose_object
from utils.config import llm_model
from utils.config import API_URL, headers
from utils.transitions import transition_state

DEBUG = True


# Handle for the input state of the app if the input is an image
async def input_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the case when the state in INPUT and we receive an image.
    """

    photo_file = await update.message.photo[-1].get_file()

    # Get the caption if it exists
    caption = update.message.caption if update.message.caption else ""

    # load image into numpy array
    tmp_photo = "app/temp_saving/tmp_photo.jpg"
    await photo_file.download_to_drive(tmp_photo)
    # img = np.array(Image.open(tmp_photo))

    # To object detection
    dict_objects = choose_object(tmp_photo, model=llm_model)

    # Print the output if DEBUG is True
    if DEBUG:
        logging.info(f"Image: {tmp_photo}")
        logging.info(f"Caption: {caption}")

    # Save the objects to the inputs list in the game state
    context.bot_data["game_state"].inputs.extend(dict_objects["object"])

    # respond photo
    await update.message.reply_text(f"Text received: {dict_objects["object"]}")


async def input_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the case when the state in INPUT and we receive a text.
    """
    # Get the text from the update
    input_text = update.message.text

    # Get the objects from the text using the LLM
    text = llm_objects_from_text(input_text)

    # Print the output if DEBUG is True
    if DEBUG:
        logging.info(f"Text: {input_text}")
        logging.info(f"Output: {text}")
    
    # Save the text to the inputs list in the game state
    context.bot_data["game_state"].inputs.extend(text)

    if len(context.bot_data["game_state"].inputs) > 2:
        await transition_state(
            update,
            context,
            State.QA,
            message=f"Got: {context.bot_data["game_state"].inputs}\nEnough inputs, now to the Q&A State!"
        )
    # respond text
    await update.message.reply_text(f"Text received: {input_text}")


async def input_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the case when the state in INPUT and we receive an audio.
    """
    audio_file = await update.message.voice.get_file()


    # load audio into numpy array
    tmp_file = "app/temp_saving/audio.wav"
    await audio_file.download_to_drive(tmp_file)

    # Get the text from the audio 
    text = audio_to_text(tmp_file)

    # Get the objects from the text using the LLM
    objects = llm_objects_from_text(text)

    # Print the output if DEBUG is True
    if DEBUG:
        logging.info(f"Audio: {tmp_file}")
        logging.info(f"Text: {text}")
        logging.info(f"Output: {objects}")

    # Save the objects to the inputs list in the game state
    context.bot_data["game_state"].inputs.extend(objects)

    # respond audio
    await update.message.reply_text(f"Text received: {text}")
