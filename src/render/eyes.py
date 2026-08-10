import random
from render.eye import Eye
from states.eye_state import EyeState
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, EYE_WIDTH, EYE_HEIGHT, EYE_SPACING, EYE_LOOK_SPEED

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

    def update(self, dt):
        self.left_eye.update(dt)
        self.right_eye.update(dt)

        self.blink_timer += dt

        if self.blink_timer >= self.next_blink:
            blink_speed = random.uniform(2.5, 4.0)
            self.left_eye.blink(blink_speed)
            self.right_eye.blink(blink_speed)

            self.blink_timer = 0.0
            self.next_blink = random.uniform(2.5, 5.0)


        if self.look_offset_x < self.target_look_offset_x:
            self.look_offset_x += EYE_LOOK_SPEED * dt

        elif self.look_offset_x > self.target_look_offset_x:
            self.look_offset_x -= EYE_LOOK_SPEED * dt

        if abs(self.target_look_offset_x - self.look_offset_x) < 1:
            self.look_offset_x = self.target_look_offset_x

        self.left_eye.x = self.left_eye_x + self.look_offset_x
        self.right_eye.x = self.right_eye_x + self.look_offset_x
        
    def draw(self, surface):
        self.left_eye.draw(surface)
        self.right_eye.draw(surface)

    def look(self, offset_x):
        self.target_look_offset_x = offset_x

    def wake_up(self):
        self.left_eye.open(5.0)
        self.right_eye.open(5.0)

    def sleep(self):
        self.left_eye.openness = 0.0
        self.right_eye.openness = 0.0

        self.left_eye.state = EyeState.IDLE
        self.right_eye.state = EyeState.IDLE