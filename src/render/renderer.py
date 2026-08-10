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
