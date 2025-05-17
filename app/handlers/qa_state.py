import logging
import re
import random
from io import BytesIO

import torch
from telegram import Update
from telegram.ext import ContextTypes
from PIL import Image
import numpy as np
import requests

from game_state import State, GameState
from utils.audio_utils import audio_to_text
from utils.character_response import send_character_response
from utils.config import *
from utils.query import *
from utils.transitions import transition_state, end_game
from utils.character_generator import EmotionalState


async def process_guess(update, context, guess_text):
    """
    Common function to process guesses from any modality.

    Args:
        update: Telegram update object
        context: Telegram context object
        guess_text: The text of the guess/question

    Returns:
        None
    """
    game_state = context.bot_data["game_state"]

    # Check for commands to change state
    if guess_text.lower() in ["restart", "new game", "quit", "exit"]:
        if game_state.secret_word:
            await end_game(update, context, win=False, chosen_object=game_state.secret_word)
        else:
            await transition_state(
                update, context, State.IDLE,
                message="Game reset. Type 'start game' to begin a new session."
            )
        return

    # Handle guesses if we're in guess mode
    if game_state.secret_word:
        # Increment attempts
        if not hasattr(game_state, 'attempts'):
            game_state.attempts = 0
        game_state.attempts += 1

        # Verify the guess
        result = verify_guess(guess_text, context)

        # Store the hint
        if not hasattr(game_state, 'hints'):
            game_state.hints = []
        game_state.hints.append(result.get('message', ''))

        # Determine emotion based on guess result
        if result.get('correct') == True:
            # Win condition
            # await send_character_response(
            #     update, context,
            #     result['message'],
            #     emotion=EmotionalState.HAPPY,
            #     additional_context="celebrating with confetti and sparkles"
            # )

            # End the game with a win
            await end_game(update, context, win=True, chosen_object=game_state.secret_word)
        else:
            # Not correct - determine emotion
            emotions = [
                EmotionalState.THOUGHTFUL,
                EmotionalState.SMUG,
                EmotionalState.CONFUSED
            ]
            emotion = random.choice(emotions)

            # Send character response with hint
            await send_character_response(
                update, context,
                result['message'],
                emotion=emotion
            )
    else:
        # Not in guess mode, prompt for image
        await send_character_response(
            update, context,
            "Let's play a guessing game! Send me an image and I'll choose an object for you to guess.",
            emotion=EmotionalState.EXCITED
        )


async def qa_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text queries in QA state"""
    query = update.message.text
    # Process the text directly
    await process_guess(update, context, query)


async def qa_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle image inputs in QA state"""
    user_id = update.message.from_user.id
    game_state = context.bot_data["game_state"]

    # Get the photo file
    photo_file = await update.message.photo[-1].get_file()
    photo_path = f"temp_saving/photo.jpg"
    await photo_file.download_to_drive(photo_path)

    # Check if we're in object selection mode or guessing mode
    if not game_state.secret_word:
        # We're in object selection mode - character chooses an object
        # Send a loading message
        message = await update.message.reply_text("Looking at the image and choosing an object...")

        # Select an object from the image
        result = choose_object(photo_path)
        chosen_object = result.get('object', '')

        # Store the chosen object and image
        game_state.secret_word = chosen_object
        if not hasattr(game_state, 'game_images'):
            game_state.game_images = []
        game_state.game_images.append(photo_path)
        game_state.attempts = 0

        # Log the chosen object (don't reveal to user)
        print(f"Chosen object for user {user_id}: {chosen_object}")

        # Delete the loading message
        await message.delete()

        # Send character response
        await send_character_response(
            update, context,
            "I've chosen an object from the image! Try to guess what it is. You can ask me yes/no questions or make guesses directly.",
            emotion=EmotionalState.THOUGHTFUL,
            additional_context="looking at an object with curiosity"
        )
    else:
        # We're in guessing mode - describe the image and use as guess
        message = await update.message.reply_text("Looking at your image to understand your guess...")

        # Use vision model to describe the image
        description = describe_image(photo_path, vision_model)

        # Update message
        await message.edit_text(f"I see: {description}")

        # Process the description as a guess
        await process_guess(update, context, description)


async def qa_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle voice inputs in QA state"""
    user_id = update.message.from_user.id

    # Get voice message
    voice_file = await update.message.voice.get_file()
    voice_path = f"./temp_saving/audio.wav"
    await voice_file.download_to_drive(voice_path)

    # Send a loading message
    message = await update.message.reply_text("Listening to your message...")

    # Here you would transcribe the voice message
    # This is a placeholder - you'd need to implement actual speech-to-text
    transcribed_text = audio_to_text(voice_path)

    # Update the loading message
    await message.edit_text(f"I heard: \"{transcribed_text}\"")

    # Process the transcribed text as a guess
    await process_guess(update, context, transcribed_text)


# Helper functions for image description and audio transcription

def describe_image(image_path, model):
    """
    Use a vision model to describe an image.

    Args:
        image_path: Path to the image file
        model: Vision model to use

    Returns:
        str: Description of the image
    """
    # For now this is a placeholder - you would integrate with your vision model
    try:
        # Encode image to base64
        base64_image = encode_image_to_base64(image_path)

        # Use Together AI vision model
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this image in a few words, focusing on visible objects. Keep it concise. Keep it only to a list of words, objects, purely. Give maximum one word only, the most prominent object. One word"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ]
        )

        # Get the description
        description = response.choices[0].message.content
        return description
    except Exception as e:
        print(f"Error describing image: {str(e)}")
        return "an image"


# def transcribe_audio(audio_path):
#     """
#     Transcribe audio to text.
#
#     Args:
#         audio_path: Path to the audio file
#
#     Returns:
#         str: Transcribed text
#     """
#     # For now this is a placeholder - you would integrate with your speech-to-text service
#     # This could be OpenAI's Whisper, Together AI's audio API, or another service
#
#     # Placeholder return
#     guesses = [
#         "Is it a chair?",
#         "Could it be a book?",
#         "I think it's a lamp",
#         "Is the object a cup?",
#         "Maybe it's a plant"
#     ]
#     return random.choice(guesses)
