import pygame
from ui.window import Window
from render.renderer import Renderer
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from events.aster_events import AsterEvent
from input.voice_input import VoiceInput
from input.voice_listener import VoiceListener
from queue import Queue
from processing.language_processor import LanguageProcessor
from actions.action_handler import ActionHandler

class AsterApp:

    def __init__(self):
        self.running = True
        self.window = Window(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            WINDOW_TITLE)
        self.renderer = Renderer()
        self.event_queue = Queue()
        self.voice_input = VoiceInput()
        self.voice_listener = VoiceListener(
            self.voice_input,
            self.event_queue
            )
        self.language_processor = LanguageProcessor()
        self.action_handler = ActionHandler()

    def run(self):
        self.window.create()

        self.voice_input.calibrate_noise()

        self.voice_listener.start()

        dt = 0.0

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.window.close()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.renderer.handle_event(AsterEvent.WAKE_UP)
            self.process_voice_events()
            self.renderer.update(dt)
            self.renderer.draw(self.window.screen)
            dt = self.window.update()

        self.voice_listener.stop()

    def process_voice_events(self):
        while not self.event_queue.empty():
            event = self.event_queue.get()

            if event["type"] == "WAKE_UP":
                self.renderer.handle_event(AsterEvent.WAKE_UP)
                text = event["text"]

                intent = self.language_processor.process(text)
                print("Intent:", intent.name)

                result = self.action_handler.execute(intent)
                print("Resultado:", result)