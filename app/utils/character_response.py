import os
import asyncio
import requests
from io import BytesIO
from utils.character_generator import EmotionalState
import random

async def send_character_response(update, context, text, emotion=None, additional_context=""):
    """
    Send a response with character image and voice message.

    Args:
        update: Telegram update object
        context: Telegram context object
        text: Text response to send
        emotion: Optional specific EmotionalState to use
        additional_context: Optional context for image generation

    Returns:
        bool: Success status
    """
    game_state = context.bot_data["game_state"]

    # Initialize character if not exists
    if not game_state.character:
        game_state.initialize_character()

    character = game_state.character

    # Select emotion if not provided
    if not emotion:
        emotions = [
            EmotionalState.HAPPY,
            EmotionalState.THOUGHTFUL,
            EmotionalState.NEUTRAL,
            EmotionalState.CURIOUS
        ]
        emotion = random.choice(emotions)

    # Send initial loading message
    loading_message = await update.message.reply_text(f"{character.name} is thinking...")

    # Generate character image with the emotion
    success, image_url = character.generate_emotional_image(
        update.message.from_user.id,
        emotion,
        context=additional_context
    )

    if success:
        try:
            # Update loading message
            await loading_message.edit_text(f"{character.name} is crafting a response...")

            # Download image
            image_response = requests.get(image_url)
            image_data = BytesIO(image_response.content)

            # Ensure temp directory exists
            os.makedirs("./temp_saving", exist_ok=True)

            # Update loading message
            await loading_message.edit_text(f"{character.name} is preparing to speak...")

            # Generate voice message
            character.generate_voice_message(text)
            voice_file_path = "./temp_saving/hint.wav"

            # Delete the loading message
            await loading_message.delete()

            # Send image with caption
            await update.message.reply_photo(
                photo=image_data,
                caption=None
            )

            # Send voice message using the file path
            with open(voice_file_path, 'rb') as voice_file:
                await update.message.reply_voice(voice_file)

            return True
        except Exception as e:
            print(f"Error in character response: {str(e)}")
            await update.message.reply_text(text)
            return False
    else:
        # Fallback to text only
        await loading_message.delete()
        await update.message.reply_text(text)
        return False
