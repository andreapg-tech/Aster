import pygame
from ui.window import Window
from render.renderer import Renderer
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from events.aster_events import AsterEvent
from input.voice_input import VoiceInput

class AsterApp:

    def __init__(self):
        self.running = True
        self.window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.renderer = Renderer()
        self.voice_input = VoiceInput()

    def run(self):
        self.window.create()

        print("Di 'Hola Aster'...")
        text = self.voice_input.listen()
        print("Has dicho:", text)

        if self.voice_input.contains_wake_word(text):
            self.renderer.handle_event(AsterEvent.WAKE_UP)

        dt = 0.0

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.window.close()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.renderer.handle_event(AsterEvent.WAKE_UP)
            self.renderer.update(dt)
            self.renderer.draw(self.window.screen)
            dt = self.window.update()