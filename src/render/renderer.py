from aster.aster import Aster
from config.settings import BACKGROUND_COLOR

class Renderer:

    def __init__(self):
        self.aster = Aster()

    def update(self, dt):
        self.aster.update(dt)

    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR)
        self.aster.draw(surface)

    def wake_up(self):
        self.aster.wake_up()

    def handle_event(self, event):
        self.aster.handle_event(event)

    def get_state(self):
        return self.aster.state