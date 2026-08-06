from render.eye import Eye
from config.settings import BACKGROUND_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT, EYE_WIDTH, EYE_HEIGHT, EYE_SPACING

class Renderer:

    def __init__(self):
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2

        left_eye_x = center_x - EYE_SPACING - EYE_WIDTH // 2
        right_eye_x = center_x + EYE_SPACING - EYE_WIDTH // 2
        eye_y = center_y - EYE_HEIGHT // 2
        
        self.left_eye = Eye(x=left_eye_x, y=eye_y, width=EYE_WIDTH, height=EYE_HEIGHT)
        self.right_eye = Eye(x=right_eye_x, y=eye_y, width=EYE_WIDTH, height=EYE_HEIGHT)

        self.left_eye.blink()
        self.right_eye.blink()
    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR) #Clean the surface.
        self.left_eye.draw(surface)
        self.right_eye.draw(surface)

    def update(self, dt):
        self.left_eye.update(dt)
        self.right_eye.update(dt)