import random
from render.eye import Eye
from config.settings import BACKGROUND_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT, EYE_WIDTH, EYE_HEIGHT, EYE_SPACING

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

    def draw(self, surface):
        self.left_eye.draw(surface)
        self.right_eye.draw(surface)
