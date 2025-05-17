from enum import Enum

from utils.character_generator import CharacterGenerator


class State(Enum):
    IDLE = 0
    INPUT = 1
    QA = 2


class GameState:
    def __init__(self, number_of_inputs=5):
        # Number of inputs before the game starts
        self.number_of_inputs = number_of_inputs

        self.state = State.INPUT
        self.inputs = []

        # Game attributes
        self.character = None
        self.secret_word = None
        self.attempts = 0
        self.last_hint = None
        self.game_images = []

        # The guesses made by the user so far
        self.guesses = []

        # Hint so far
        self.hints = []

    def transition_to(self, new_state, context=None):
        """Transition to a new state with optional context data"""
        old_state = self.state
        self.state = new_state

        # Reset game attributes if transitioning to IDLE
        if new_state == State.IDLE:
            self.reset_game()

        print(f"State transition: {old_state} -> {new_state}")
        return self.state

    def reset_game(self):
        """Reset all game-related attributes"""
        self.state = State.INPUT
        self.inputs = []

        # Game attributes
        self.character = None
        self.secret_word = None
        self.attempts = 0
        self.last_hint = None
        self.game_images = []

        # The guesses made by the user so far
        self.guesses = []

        # Hint so far
        self.hints = []

    def initialize_character(self, name="Riddlemaster"):
        """Initialize a new character"""
        self.character = CharacterGenerator()
        self.character.set_name(name)
        return self.character

    def get_state(self):
        """Get the current state"""
        return self.state
