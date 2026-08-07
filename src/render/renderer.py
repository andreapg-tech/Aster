from render.eyes import Eyes
from config.settings import BACKGROUND_COLOR

class Renderer:

    def __init__(self):
        self.eyes = Eyes()

    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR) #Clean the surface.
        self.eyes.draw(surface)

    def update(self, dt):
        self.eyes.update(dt)