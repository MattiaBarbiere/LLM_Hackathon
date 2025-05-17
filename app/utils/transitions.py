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

        # Perform the transition
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
