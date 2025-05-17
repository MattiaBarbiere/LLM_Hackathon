from game_state import State
from telegram.ext import MessageHandler, filters, ConversationHandler


class StateHandlerFactory:
    def __init__(self, application):
        self.application = application
        self.handlers = {}
        self.current_handlers = []

    def register_handler(self, state, message_filter, handler_function):
        """Register a handler for a specific state and message filter"""
        if state not in self.handlers:
            self.handlers[state] = []

        self.handlers[state].append((message_filter, handler_function))

    def update_handlers(self, new_state):
        """Update active handlers based on the new state"""
        # Remove current handlers
        for handler in self.current_handlers:
            self.application.remove_handler(handler)

        self.current_handlers = []

        # Add new handlers for the current state
        if new_state in self.handlers:
            for message_filter, handler_function in self.handlers[new_state]:
                handler = MessageHandler(message_filter, handler_function)
                self.application.add_handler(handler)
                self.current_handlers.append(handler)

        return len(self.current_handlers) > 0
