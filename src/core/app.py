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
from states.aster_state import AsterState

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

        self.pending_text = None

        self.sleep_delay = 3.0
        self.sleep_timer = 0.0

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
                
            self.process_voice_events()
            self.update_wake_up()
            self.update_sleep_timer(dt)
            self.update_conversation_timer(dt)

            self.renderer.update(dt)
            self.renderer.draw(self.window.screen)
            dt = self.window.update()

        self.voice_listener.stop()
        self.window.close()


    def process_voice_events(self):
        while not self.event_queue.empty():
            event = self.event_queue.get()

            if event["type"] == "WAKE_UP":
                self.voice_listener.pause()
                self.renderer.handle_event(AsterEvent.WAKE_UP)
                self.pending_text = event["text"]

            elif event["type"] == "CONVERSATION_INPUT":
                self.voice_listener.pause()
                self.conversation_timer = 0.0
                text = event["text"]
                self.process_text(text)   

            elif event["type"] == "PROCESSING_FINISHED":
                result = event["result"]
                intent = event["intent"]
                was_conversing = event["was_conversing"]

                if result:
                    self.continue_conversation = (intent.name == "conversation" or was_conversing)
                    self.conversation_timer = 0.0
                    self.renderer.handle_event(AsterEvent.START_SPEAKING)
                    self.speech_service.speak(result)
                
                    threading.Thread(
                        target=self.wait_for_speech,
                        daemon=True
                    ).start()
                else:
                    self.voice_listener.resume()
                    self.renderer.handle_event(AsterEvent.START_LISTENING)

            elif event["type"] == "SPEECH_FINISHED":
                if self.continue_conversation:
                    self.voice_listener.start_conversation()
                    self.renderer.handle_event(AsterEvent.START_LISTENING)
                else:
                    self.renderer.handle_event(AsterEvent.FINISH_SPEAKING)
                self.voice_listener.resume()   

    def wait_for_speech(self):
        while self.speech_service.is_speaking():
            time.sleep(0.1)

        self.event_queue.put({
            "type": "SPEECH_FINISHED"
        })

    def process_text(self, text):
        was_conversing = self.voice_listener.conversation_mode

        self.renderer.handle_event(AsterEvent.START_PROCESSING)

        threading.Thread(
            target=self._bg_process_text,
            args=(text, was_conversing),
            daemon=True
        ).start()

    def _bg_process_text(self, text, was_conversing):
        intent = self.language_processor.process(text)
        print("Intent:", intent.name)
        
        result = self.action_handler.execute(intent)
        print("Resultado:", result)

        #Save history
        if result:
            import json
            structured_response = json.dumps({
                "intent": intent.name,
                "parameters": {
                    "response": result
                }
            }, ensure_ascii=False)
            self.language_processor.add_to_history("user", text)
            self.language_processor.add_to_history("assistant", structured_response)
        
        self.event_queue.put({
            "type": "PROCESSING_FINISHED",
            "result": result,
            "intent": intent,
            "was_conversing": was_conversing
        })

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
            self.renderer.handle_event(AsterEvent.FINISH_SPEAKING)

    def update_wake_up(self):
        if self.pending_text is None:
            return

        if self.renderer.get_state() == AsterState.WAKE_UP:
            return

        text = self.pending_text
        self.pending_text = None

        self.process_text(text)

    def update_sleep_timer(self, dt):
        if self.renderer.get_state() != AsterState.IDLE:
            self.sleep_timer = 0.0
            return

        if self.voice_listener.conversation_mode:
            self.sleep_timer = 0.0
            return

        self.sleep_timer += dt

        if self.sleep_timer >= self.sleep_delay:
            self.sleep_timer = 0.0
            self.renderer.handle_event(AsterEvent.SLEEP)