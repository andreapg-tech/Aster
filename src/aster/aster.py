import random
from render.eyes import Eyes
from states.aster_state import AsterState
from config.settings import WAKE_UP_DURATION

class Aster:

    def __init__(self):
        self.state = AsterState.SLEEPING
        self.eyes = Eyes()
        self.eyes.sleep()

        self.look_timer = 0.0
        self.next_look = random.uniform(3.0, 6.0)
        self.current_look = 0

        self.wake_up_timer = 0.0

    def update(self, dt):
        if self.state == AsterState.SLEEPING:
            pass

        elif self.state == AsterState.WAKE_UP:
            self.eyes.update(dt)
            self.wake_up_timer += dt

            if self.wake_up_timer >= WAKE_UP_DURATION:
                self.state = AsterState.IDLE

        elif self.state == AsterState.IDLE:
            self.eyes.update(dt)
            self.look_timer += dt

            if self.look_timer >= self.next_look:
                possible_looks = [-40, 0, 40]
                possible_looks.remove(self.current_look)

                look_offset = random.choice([-40, 0, 40])

                self.eyes.look(look_offset)
                self.current_look = look_offset

                self.look_timer = 0.0
                self.next_look = random.uniform(3.0, 6.0)

    def draw(self, surface):
        self.eyes.draw(surface)

    def wake_up(self):
        if self.state == AsterState.SLEEPING:
            self.state = AsterState.WAKE_UP
            self.wake_up_timer = 0.0
            self.eyes.wake_up()