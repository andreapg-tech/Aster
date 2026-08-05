import pygame
from config.settings import EYE_COLOR

class Eye:
    """Draw all the visual elements."""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.heigh = height

    def draw(self, surface):
        pygame.draw.ellipse(surface, EYE_COLOR, (self.x, self.y, self.width, self.heigh))