from enum import Enum


class State(Enum):
    IDLE = 0
    INPUT = 1
    QA = 2


class GameState:
    state: State = State.IDLE

    inputs: list = []
