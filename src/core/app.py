import pygame
from ui.window import Window
from render.renderer import Renderer

class AsterApp:

    def __init__(self):
        self.running = True
        self.window = Window(800, 600, "Aster")
        self.renderer = Renderer()

    def run(self):
        self.window.create()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.window.close()

            self.renderer.draw(self.window.screen)
            self.window.update()