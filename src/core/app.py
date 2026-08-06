import pygame
from ui.window import Window
from render.renderer import Renderer
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE

class AsterApp:

    def __init__(self):
        self.running = True
        self.window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.renderer = Renderer()

    def run(self):
        self.window.create()

        dt = 0.0

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.window.close()
            self.renderer.update(dt)
            self.renderer.draw(self.window.screen)
            dt = self.window.update()