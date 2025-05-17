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

    # Generate character image with the emotion
    success, image_url = character.generate_emotional_image(
        update.message.from_user.id,
        emotion,
        context=additional_context
    )

    if success:
        try:
            # Download image
            image_response = requests.get(image_url)
            image_data = BytesIO(image_response.content)

            # Generate voice message
            voice_message = character.generate_voice_message(text)

            # Send image with caption
            await update.message.reply_photo(
                photo=image_data,
                # caption=voice_message
            )

            # Send voice message (placeholder)
            # await update.message.reply_text(f"🔊 {voice_message}")

            return True
        except Exception as e:
            print(f"Error in character response: {str(e)}")
            await update.message.reply_text(text)
            return False
    else:
        # Fallback to text only
        await update.message.reply_text(text)
        return False
