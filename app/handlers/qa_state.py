import logging
import re

import torch
from telegram import Update
from telegram.ext import ContextTypes
from PIL import Image
import numpy as np

from game_state import State, GameState
from utils.character_response import send_character_response
from utils.config import *
from utils.query import *
from utils.transitions import transition_state
import random
import json
from telegram import Update
from telegram.ext import ContextTypes
from game_state import State
from utils.query import verify_guess
from utils.transitions import transition_state
from utils.character_generator import EmotionalState


async def qa_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text queries in QA state"""
    query = update.message.text
    user_id = update.message.from_user.id
    game_state = context.bot_data["game_state"]

    # Check for commands to change state
    if query.lower() in ["restart", "new game", "quit", "exit"]:
        message = "Game reset."
        if game_state.secret_word:
            message = f"Game over. The object was: {game_state.secret_word}. {message}"

        await transition_state(
            update, context, State.IDLE,
            message=message + " Type 'start game' to begin a new session."
        )
        return

    # Handle guesses if we're in guess mode
    if game_state.secret_word:
        # Increment attempts
        game_state.attempts += 1

        # Verify the guess
        result = verify_guess(query, game_state.secret_word)
        game_state.last_hint = result.get('message', '')

        # Determine emotion based on guess result
        emotion = EmotionalState.NEUTRAL
        additional_context = ""

        if result.get('correct') == True:
            emotion = EmotionalState.HAPPY
            additional_context = "celebrating with confetti and sparkles"
        else:
            # Varying degrees of emotion based on how close they might be
            emotions = [
                EmotionalState.THOUGHTFUL,
                EmotionalState.SMUG,
                EmotionalState.CONFUSED
            ]
            emotion = random.choice(emotions)

        # Send character response
        await send_character_response(
            update, context,
            result['message'],
            emotion=emotion,
            additional_context=additional_context
        )

        # If correct or too many attempts, transition back to IDLE
        if result.get('correct') == True or game_state.attempts >= 5:
            await transition_state(
                update, context, State.IDLE,
                message="Type 'start game' to play again."
            )
    else:
        # Not in guess mode, prompt for image
        await send_character_response(
            update, context,
            "Let's play a guessing game! Send me an image and I'll choose an object for you to guess.",
            emotion=EmotionalState.EXCITED
        )


async def qa_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle image inputs in QA state - used to start the object guessing game"""
    user_id = update.message.from_user.id
    game_state = context.bot_data["game_state"]

    # Get the photo file
    photo_file = await update.message.photo[-1].get_file()
    photo_path = f"temp/photo_{user_id}.jpg"
    await photo_file.download_to_drive(photo_path)

    # Send a loading message
    message = await update.message.reply_text("Looking at the image and choosing an object...")

    # Select an object from the image
    result = choose_object(photo_path, "meta-llama/Meta-Llama-3.1-Vision-8B")
    chosen_object = result.get('object', '')

    # Store the chosen object and image
    game_state.secret_word = chosen_object
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


async def qa_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle voice inputs in QA state"""
    user_id = update.message.from_user.id
    game_state = context.bot_data["game_state"]

    # Get voice message
    voice_file = await update.message.voice.get_file()
    voice_path = f"temp/voice_{user_id}.ogg"
    await voice_file.download_to_drive(voice_path)

    # Send a loading message
    message = await update.message.reply_text("Listening to your message...")

    # Here you would transcribe the voice message
    # This is a placeholder - you'd need to implement actual speech-to-text
    transcribed_text = "What is the object you're thinking of?"

    # Update the loading message
    await message.edit_text(f"I heard: \"{transcribed_text}\"")

    # Craft response based on game state
    if game_state.secret_word:
        response_text = "I heard your question. To guess the object, please type your guess."
    else:
        response_text = "I heard you! Send me an image first so I can choose an object for you to guess."

    # Send character response
    await send_character_response(
        update, context,
        response_text,
        emotion=EmotionalState.CURIOUS
    )
