import pygame

class Window:

    def __init__(self, width: int, height: int, title: str):
        self.width = width
        self.height = height
        self.title = title
        self.screen = None #Store the rendering surface so other components can draw on it.
        self.clock = pygame.time.Clock()

    def create(self):
        """Initialize Pygame and create the application window."""

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def update(self):
        pygame.display.flip()
        dt = self.clock.tick(60) / 1000
        return dt

    def close(self):
        pygame.quit()