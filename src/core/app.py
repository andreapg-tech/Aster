import pygame
import threading
import time
from ui.window import Window
from render.renderer import Renderer
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from events.aster_events import AsterEvent
from input.voice_input import VoiceInput
from input.voice_listener import VoiceListener
from queue import Queue
from processing.language_processor import LanguageProcessor
from actions.action_handler import ActionHandler
from services.speech_service import SpeechService

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
        self.speech_service = SpeechService()

        self.conversation_time_out = 10.0
        self.conversation_timer = 0.0

        self.continue_conversation = False

    def run(self):
        self.window.create()

        self.language_processor.warm_up()

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
            self.update_conversation_timer(dt)

            self.renderer.update(dt)
            self.renderer.draw(self.window.screen)
            dt = self.window.update()

        self.voice_listener.stop()

    def process_voice_events(self):
        while not self.event_queue.empty():
            event = self.event_queue.get()

            if event["type"] == "WAKE_UP":
                self.voice_listener.pause()

                self.renderer.handle_event(AsterEvent.WAKE_UP)
                text = event["text"]

                self.process_text(text)

            elif event["type"] == "CONVERSATION_INPUT":
                self.voice_listener.pause()

                self.conversation_timer = 0.0

                text = event["text"]
                
                self.process_text(text)      

    def wait_for_speech(self):
        while self.speech_service.is_speaking():
            time.sleep(0.1)

        if self.continue_conversation:
            self.voice_listener.start_conversation()

        self.voice_listener.resume()

    def process_text(self, text):
        was_conversing = self.voice_listener.conversation_mode

        intent = self.language_processor.process(text)
        print("Intent:", intent.name)
        
        result = self.action_handler.execute(intent)
        print("Resultado:", result)
        
        if result:
            self.continue_conversation = (intent.name == "conversation" or was_conversing)
            self.conversation_timer = 0.0
            self.speech_service.speak(result)
        
            threading.Thread(
                target=self.wait_for_speech,
                daemon=True
            ).start()

        else:
            self.voice_listener.resume()

    def update_conversation_timer(self, dt):
        if not self.voice_listener.conversation_mode:
            return

        if self.speech_service.is_speaking():
            return

        self.conversation_timer += dt

        if self.conversation_timer >= self.conversation_time_out:
            self.voice_listener.end_conversation()
            self.language_processor.clear_conversation()
            self.conversation_timer = 0.0
            self.continue_conversation = False