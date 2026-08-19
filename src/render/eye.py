import pygame
from config.settings import EYE_COLOR
from states.eye_state import EyeState


class Eye:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.openness = 1.0
        self.state = EyeState.IDLE
        self.animation_speed = 0.0

    def draw(self, surface):
        current_height = int(self.height * self.openness)

        if current_height <= 6:
            line_y = self.y + self.height // 2

            pygame.draw.line(
                surface,
                EYE_COLOR,
                (
                    self.x + 8,
                    line_y
                ),
                (
                    self.x + self.width - 8,
                    line_y
                ),
                6
            )

            return

        height_difference = self.height - current_height
        current_y = self.y + height_difference // 2

        pygame.draw.ellipse(
            surface,
            EYE_COLOR,
            (
                self.x,
                current_y,
                self.width,
                current_height
            )
        )

    def update(self, dt):
        if self.state == EyeState.CLOSING:
            self.openness -= self.animation_speed * dt

            if self.openness <= 0.0:
                self.openness = 0.0
                self.state = EyeState.OPENING

        elif self.state == EyeState.OPENING:
            self.openness += self.animation_speed * dt

            if self.openness >= 1.0:
                self.openness = 1.0
                self.state = EyeState.IDLE

        elif self.state == EyeState.SLEEPING:
            self.openness -= self.animation_speed * dt

            if self.openness <= 0.0:
                self.openness = 0.0

    def blink(self, speed):
        if self.state == EyeState.IDLE:
            self.state = EyeState.CLOSING
            self.animation_speed = speed

    def open(self, speed):
        if self.openness < 1.0:
            self.animation_speed = speed
            self.state = EyeState.OPENING

    def sleep(self, speed):
        if self.openness > 0.0:
            self.animation_speed = speed
            self.state = EyeState.SLEEPING

    def is_closed(self):
        return self.openness <= 0.0