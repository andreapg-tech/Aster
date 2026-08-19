import random
from render.eye import Eye
from states.eye_state import EyeState
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, EYE_WIDTH, EYE_HEIGHT, EYE_SPACING, EYE_LOOK_SPEED
from states.aster_state import AsterState

class Eyes:

    def __init__(self):
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
    
        left_eye_x = center_x - EYE_SPACING - EYE_WIDTH // 2
        right_eye_x = center_x + EYE_SPACING - EYE_WIDTH // 2
        eye_y = center_y - EYE_HEIGHT // 2
                
        self.left_eye = Eye(x=left_eye_x, y=eye_y, width=EYE_WIDTH, height=EYE_HEIGHT)
        self.right_eye = Eye(x=right_eye_x, y=eye_y, width=EYE_WIDTH, height=EYE_HEIGHT)

        self.blink_timer = 0.0
        self.next_blink = random.uniform(2.5, 5.0)

        self.left_eye_x = left_eye_x
        self.right_eye_x = right_eye_x
        self.look_offset_x = 0.0 #Current position
        self.target_look_offset_x = 0.0 #Position we want to reach

        self.current_look = 0

        self.look_timer = 0.0
        self.next_look = random.uniform(3.0, 6.0)

        self.aster_state = AsterState.SLEEPING

    def update(self, dt):
        self.left_eye.update(dt)
        self.right_eye.update(dt)

        if self.aster_state != AsterState.SLEEPING:
            self.blink_timer += dt
            if self.blink_timer >= self.next_blink:
                blink_speed = random.uniform(2.5, 4.0)

                self.left_eye.blink(blink_speed)
                self.right_eye.blink(blink_speed)

                self.blink_timer = 0.0
                self.next_blink = random.uniform(2.5, 5.0)

            if self.aster_state == AsterState.IDLE:
                self._update_idle_look(dt)

            elif self.aster_state == AsterState.LISTENING:
                self._update_listening_look(dt)

            elif self.aster_state == AsterState.PROCESSING:
                self._update_processing_look(dt)

            elif self.aster_state == AsterState.SPEAKING:
                self._update_speaking_look(dt)

            self._update_eye_positions(dt)
        
    def draw(self, surface):
        self.left_eye.draw(surface)
        self.right_eye.draw(surface)

    def look(self, offset_x):
        self.target_look_offset_x = offset_x

    def wake_up(self):
        self.look_offset_x = 0.0
        self.target_look_offset_x = 0.0

        self.left_eye.x = self.left_eye_x
        self.right_eye.x = self.right_eye_x

        self.left_eye.open(5.0)
        self.right_eye.open(5.0)

    def sleep(self):
        sleep_speed = 2.0

        self.left_eye.sleep(sleep_speed)
        self.right_eye.sleep(sleep_speed)

    def start_listening(self):
        self.look_timer = 0.0
        self.next_look = 1.0
        self.look(-20)
        self.current_look = -20

    def start_processing(self):
        self.look_timer = 0.0
        self.next_look = 0.7
        self.look(30)
        self.current_look = 30

    def start_speaking(self):
        self.look_timer = 0.0
        self.next_look = 1.0
        self.look(0)
        self.current_look = 0

    def reset_look(self):
        self.look(0)
        self.current_look = 0
        self.look_timer = 0.0
        self.next_look = random.uniform(3.0, 6.0)

    def _update_idle_look(self, dt):
        self.look_timer += dt

        if self.look_timer >= self.next_look:
            possible_looks = [-40, 0, 40]
            possible_looks.remove(self.current_look)

            look_offset = random.choice(possible_looks)

            self.look(look_offset)
            self.current_look = look_offset

            self.look_timer = 0.0
            self.next_look = random.uniform(3.0, 6.0)

    def _update_listening_look(self, dt):
        self.look_timer += dt

        if self.look_timer >= self.next_look:
            possible_looks = [-20, 0, 20]

            if self.current_look in possible_looks:
                possible_looks.remove(self.current_look)

            look_offset = random.choice(possible_looks)

            self.look(look_offset)
            self.current_look = look_offset

            self.look_timer = 0.0
            self.next_look = random.uniform(0.8, 1.5)

    def _update_processing_look(self, dt):
        self.look_timer += dt

        if self.look_timer >= self.next_look:
            if self.current_look <= 0:
                look_offset = 30
            else:
                look_offset = -30

            self.look(look_offset)
            self.current_look = look_offset

            self.look_timer = 0.0
            self.next_look = random.uniform(0.6, 1.0)

    def _update_speaking_look(self, dt):
        self.look_timer += dt

        if self.look_timer >= self.next_look:
            look_offset = random.choice([-15, 0, 15])

            self.look(look_offset)
            self.current_look = look_offset

            self.look_timer = 0.0
            self.next_look = random.uniform(1.0, 2.0)

    def _update_eye_positions(self, dt):
        difference = self.target_look_offset_x - self.look_offset_x

        if abs(difference) <= 1:
            self.look_offset_x = self.target_look_offset_x

        else:
            movement = EYE_LOOK_SPEED * dt

            if difference > 0:
                self.look_offset_x += min(movement, difference)
            else:
                self.look_offset_x -= min(movement, -difference)

        self.left_eye.x = self.left_eye_x + self.look_offset_x
        self.right_eye.x = self.right_eye_x + self.look_offset_x

    def set_state(self, state):
        self.aster_state = state
        self.look_timer = 0.0
        self.current_look = 0

    def is_closed(self):
        return (
            self.left_eye.is_closed()
            and self.right_eye.is_closed()
        )