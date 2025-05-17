import logging
from telegram import Update
from telegram.ext import ContextTypes
from PIL import Image
import numpy as np

# Together.ai imports
from together import Together
from keys import TOGETHER_AI

# auth defaults to os.environ.get("TOGETHER_API_KEY")
client = Together(
    api_key=TOGETHER_AI,
)


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

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
        messages=[
            {"role": "system", "content": "You are given a prompt from the user. You must take that prompt and "
                                          "answer back the list of objects that were written in the prompt. They must be separated by commas."
                                          "Your answer must be in the format: 'object1, object2, object3'."},
            {"role": "user", "content": f"{input_text}"},
        ]
    )
    text = response.choices[0].message.content.split(", ")

    # Save the text to the inputs list in the game state
    context.bot_data["game_state"].inputs.extend(text)

    # respond text
    await update.message.reply_text(f"Text received: {input_text}")
