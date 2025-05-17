import logging
from telegram import Update
from telegram.ext import ContextTypes

from game_state import State
# Our imports
from utils.LLM_utils import llm_objects_from_text
from utils.audio_utils import audio_to_text
from utils.query import choose_object
from utils.config import llm_model
from utils.transitions import transition_state
from utils.input_utils import check_input_length

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
    object_from_image = choose_object(tmp_photo, model=llm_model)["object"]

    # Get the objects from the image using the LLM
    objects_from_caption = llm_objects_from_text(caption)

    # Print the output if DEBUG is True
    if DEBUG:
        logging.info(f"Image: {tmp_photo}")
        logging.info(f"Caption: {caption}")

    object_and_caption = [*objects_from_caption, object_from_image]

    # Save the objects to the inputs list in the game state
    context.bot_data["game_state"].inputs.extend(object_and_caption)

    # Respond to the user
    await check_input_length(update, context)


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

    # Respond to the user
    await check_input_length(update, context)


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

    # Respond to the user
    await check_input_length(update, context)
