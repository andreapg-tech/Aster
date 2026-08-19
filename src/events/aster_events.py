from enum import Enum

class AsterEvent(Enum):
    WAKE_UP = 1
    START_LISTENING = 2
    START_PROCESSING = 3
    START_SPEAKING = 4
    FINISH_SPEAKING = 5
    SLEEP = 6