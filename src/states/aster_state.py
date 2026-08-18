from enum import Enum

class AsterState(Enum):
    SLEEPING = 1
    WAKE_UP = 2
    IDLE = 3
    LISTENING = 4
    PROCESSING = 5
    SPEAKING = 6