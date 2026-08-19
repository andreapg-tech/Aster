from render.eyes import Eyes
from states.aster_state import AsterState
from config.settings import WAKE_UP_DURATION
from events.aster_events import AsterEvent

class Aster:

    def __init__(self):
        self.state = AsterState.SLEEPING
        self.eyes = Eyes()
        self.eyes.sleep()

        self.wake_up_timer = 0.0

    def update(self, dt):
        if self.state == AsterState.SLEEPING:
            return

        if self.state == AsterState.WAKE_UP:
            self.eyes.update(dt)
            self.wake_up_timer += dt

            if self.wake_up_timer >= WAKE_UP_DURATION:
                self.state = AsterState.IDLE
                self.eyes.set_state(self.state)

            return

        self.eyes.update(dt)

    def draw(self, surface):
        self.eyes.draw(surface)

    def wake_up(self):
        if self.state == AsterState.SLEEPING:
            self.state = AsterState.WAKE_UP
            self.wake_up_timer = 0.0

            self.eyes.set_state(self.state)
            self.eyes.wake_up()

    def handle_event(self, event):
        if event == AsterEvent.WAKE_UP:
            self.wake_up()

        elif event == AsterEvent.START_LISTENING:
            self.state = AsterState.LISTENING
            self.eyes.set_state(self.state)
            self.eyes.start_listening()

        elif event == AsterEvent.START_PROCESSING:
            self.state = AsterState.PROCESSING
            self.eyes.set_state(self.state)
            self.eyes.start_processing()

        elif event == AsterEvent.START_SPEAKING:
            self.state = AsterState.SPEAKING
            self.eyes.set_state(self.state)
            self.eyes.start_speaking()

        elif event == AsterEvent.FINISH_SPEAKING:
            self.state = AsterState.IDLE
            self.eyes.set_state(self.state)
            self.eyes.reset_look()