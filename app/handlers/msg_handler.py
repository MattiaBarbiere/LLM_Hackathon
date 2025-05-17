import logging
from telegram import Update
from telegram.ext import ContextTypes
from PIL import Image
import numpy as np

import audiofile
from pdfrw import PdfReader

# Together.ai imports
from together import Together

from handlers.qa_state import qa_text
from keys import TOGETHER_AI
from game_state import State

from handlers.input_state import input_text

# auth defaults to os.environ.get("TOGETHER_API_KEY")
client = Together(
    api_key=TOGETHER_AI,
)


async def msg_handler_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Router for messages"""

    game_state = context.bot_data["game_state"]

    if game_state.state == State.INPUT:
        await input_text(update, context)
    elif game_state.state == State.QA:
        await qa_text(update, context)
    else:
        await update.message.reply_text(f"got text: {update.message.text}")


async def msg_handler_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Router for messages"""
    photo_file = await update.message.photo[-1].get_file()

    # load image into numpy array
    tmp_photo = "tmp_photo.jpg"
    await photo_file.download_to_drive(tmp_photo)
    img = np.array(Image.open(tmp_photo))

    # if state == State.INPUT:
    #     await input_text(update, context)
    # elif state == State.QA:
    #     await qa_text(update, context)
    await update.message.reply_photo(tmp_photo, caption=f"Image shape: {img.shape}")


async def msg_handler_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Router for voice"""
    audio_file = await update.message.voice.get_file()

    # load audio into numpy array
    tmp_file = "voice_note.wav"
    await audio_file.download_to_drive(tmp_file)

    signal, sampling_rate = audiofile.read(tmp_file, always_2d=True)
    duration = signal.shape[1] / sampling_rate

    # await update.message.reply_voice(tmp_file, caption=f"Voice note duration: {duration} seconds")


async def msg_handler_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Router for audio"""

    audio_file = await update.message.audio.get_file()

    # load audio into numpy array
    tmp_file = "audio.wav"
    await audio_file.download_to_drive(tmp_file)

    signal, sampling_rate = audiofile.read(tmp_file, always_2d=True)
    duration = signal.shape[1] / sampling_rate

    # respond audio
    # await update.message.reply_audio(tmp_file, caption=f"Audio duration: {duration} seconds")


async def msg_handler_attachment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Router for attachments"""

    attachment_file = await update.message.document.get_file()

    # download pdf and send back
    tmp_file = "attachment.pdf"
    await attachment_file.download_to_drive(tmp_file)

    # read PDF
    reader = PdfReader(tmp_file)

    # get title and number of pagers
    title = reader.Info.Title
    num_pages = len(reader.pages)

    # respond attachment
    # await update.message.reply_document(tmp_file, caption=f"PDF title: {title}, number of pages: {num_pages}")
