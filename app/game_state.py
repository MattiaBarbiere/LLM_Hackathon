from enum import Enum


class State(Enum):
    IDLE = 0
    INPUT = 1
    QA = 2


class GameState:
    def __init__(self):
        self.state = State.IDLE
        self.inputs = []
        self.context = {}  # Additional context data for the current state

    def transition_to(self, new_state, context=None):
        """Transition to a new state with optional context data"""
        old_state = self.state
        self.state = new_state

        if context:
            self.context.update(context)

        print(f"State transition: {old_state} -> {new_state}")
        return self.state

    def get_state(self):
        """Get the current state"""
        return self.state
