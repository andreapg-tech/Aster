import pygame

class Window:

    def __init__(self, width: int, height: int, title: str):
        self.width = width
        self.height = height
        self.title = title
        self.screen = None #Store the rendering surface so other components can draw on it.

    def create(self):
        """Initialize Pygame and create the application window."""

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def update(self):
        pass

    def close(self):
        pygame.quit()