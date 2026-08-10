import random
from render.eyes import Eyes
from states.aster_state import AsterState

class Aster:

    def __init__(self):
        self.state = AsterState.IDLE
        self.eyes = Eyes()

        self.look_timer = 0.0
        self.next_look = random.uniform(3.0, 6.0)

        self.current_look = 0

    def update(self, dt):
        if self.state == AsterState.IDLE:
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