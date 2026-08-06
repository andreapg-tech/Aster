import pygame
import random
from config.settings import EYE_COLOR, EYE_BLINK_SPEED
from states.eye_state import EyeState

class Eye:
    """Draw all the visual elements."""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.openness = 1.0
        self.state = EyeState.IDLE

    def draw(self, surface):
        current_height = int(self.height * self.openness)

        height_difference = self.height - current_height
        current_y = self.y + height_difference // 2
        
        pygame.draw.ellipse(surface, EYE_COLOR, (self.x, current_y, self.width, current_height))

    def update(self, dt):
        if self.state == EyeState.CLOSING:
            self.openness -= EYE_BLINK_SPEED * dt
            if self.openness <= 0.0:
                self.openness = 0.0
                self.state = EyeState.OPENING

        elif self.state == EyeState.OPENING:
            self.openness += EYE_BLINK_SPEED * dt
            if self.openness >= 1.0:
                self.openness = 1.0
                self.state = EyeState.IDLE

        elif self.state == EyeState.IDLE:
            pass

    def blink(self):
        if self.state == EyeState.IDLE:
            self.state = EyeState.CLOSING