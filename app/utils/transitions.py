import random

from game_state import State
import requests
from io import BytesIO
from utils.character_generator import EmotionalState

# Helper function for character responses (you can also put this in a separate file)
async def send_character_response(update, context, text, emotion=None, additional_context=""):
    """
    Send a response with character image and voice message.
    """
    game_state = context.bot_data["game_state"]

    # Initialize character if not exists
    if not game_state.character:
        # Create and initialize the character
        from utils.character_generator import CharacterGenerator
        game_state.character = CharacterGenerator()
        game_state.character.set_name("Riddlemaster")

    character = game_state.character

    # Select emotion if not provided
    if not emotion:
        import random
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
                caption=text
            )

            # Send voice message (placeholder)
            await update.message.reply_text(f"🔊 {voice_message}")

            return True
        except Exception as e:
            print(f"Error in character response: {str(e)}")
            await update.message.reply_text(text)
            return False
    else:
        # Fallback to text only
        await update.message.reply_text(text)
        return False


async def transition_to_qa_with_character(update, context, message=None):
    """Transition to QA state and initialize a character"""
    game_state = context.bot_data["game_state"]
    state_handler = context.bot_data["state_handler"]

    # Create a new character if one doesn't exist
    if not game_state.character:
        from utils.character_generator import CharacterGenerator
        game_state.character = CharacterGenerator()
        game_state.character.set_name("Riddlemaster")

    # Perform the transition
    game_state.transition_to(State.QA)
    state_handler.update_handlers(State.QA)

    # Get welcome message
    welcome_text = message if message else "I am your guide for this game. Try to guess what I'm thinking of!"

    # Send character response with welcome message
    await send_character_response(
        update,
        context,
        welcome_text,
        emotion=EmotionalState.HAPPY
    )

    return True


async def transition_state(update, context, target_state, message=None):
    """
    Transition to a new state and update handlers.

    Args:
        update: The Telegram update object
        context: The Telegram context object
        target_state: The state to transition to
        message: Optional message to send to the user

    Returns:
        bool: True if transition was successful
    """
    try:
        game_state = context.bot_data["game_state"]
        state_handler = context.bot_data["state_handler"]

        # Perform the transition (this will reset if going to IDLE)
        game_state.transition_to(target_state)

        # Update the handlers
        state_handler.update_handlers(target_state)

        # Send a message if provided
        if message:
            await update.message.reply_text(message)

        return True
    except Exception as e:
        print(f"Error during state transition: {str(e)}")
        return False


async def end_game(update, context, win=False, chosen_object=None):
    """
    End the game with appropriate celebration or commiseration
    """
    game_state = context.bot_data["game_state"]

    # Save the object for reference
    if not chosen_object and game_state.secret_word:
        chosen_object = game_state.secret_word

    if win:
        # Create winning celebration response
        emotion = EmotionalState.HAPPY
        additional_context = "celebrating with confetti and sparkles in a victory pose"

        # Different winning messages for variety
        win_messages = [
            f"🎉 Congratulations! You correctly guessed that the object was '{chosen_object}'! You're really observant!",
            f"🏆 Well done! '{chosen_object}' is exactly right! You've got a good eye!",
            f"✨ Amazing! You figured out it was '{chosen_object}'! I'm impressed by your deduction skills!"
        ]
        message = random.choice(win_messages)

        # Send celebratory character response
        await send_character_response(
            update, context, message, emotion, additional_context
        )

    else:
        # Create commiseration response
        emotion = EmotionalState.THOUGHTFUL
        additional_context = "looking slightly disappointed but encouraging"

        # Different losing messages
        lose_messages = [
            f"Game over! The object I chose was '{chosen_object}'. Better luck next time!",
            f"Time's up! I was thinking of '{chosen_object}'. Maybe you'll guess it next time!",
            f"That was a tough one! The object was '{chosen_object}'. Want to try again with a new image?"
        ]
        message = random.choice(lose_messages)

        # Send commiseration character response
        await send_character_response(
            update, context, message, emotion, additional_context
        )

    # Wait a moment for the user to read the message
    import asyncio
    await asyncio.sleep(2)

    # Transition to IDLE state
    await transition_state(
        update, context, State.IDLE,
        message="Type 'start game' or send an image to play again."
    )
