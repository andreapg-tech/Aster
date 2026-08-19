import threading
import time

class VoiceListener:

    def __init__(self, voice_input, event_queue):
        self.voice_input = voice_input
        self.event_queue = event_queue

        self.running = False
        self.listening = False

        self.thread = None

        self.conversation_mode = False

    def start(self):
        self.running = True
        self.listening = True

        self.thread = threading.Thread(
            target=self._listen_loop,
            daemon=True
        )

        self.thread.start()

    def _listen_loop(self):
        while self.running:
            if not self.listening:
                time.sleep(0.1)
                continue

            text = self.voice_input.listen()

            if not text:
                continue

            if self.conversation_mode:
                self.listening = False
                
                self.event_queue.put({
                    "type": "CONVERSATION_INPUT",
                    "text": text
                })

            elif self.voice_input.contains_wake_word(text):
                print("¡Wake word detectada!")

                self.listening = False

                self.event_queue.put({
                    "type": "WAKE_UP",
                    "text": text
                })

    def pause(self):
        self.listening = False

    def resume(self):
        self.listening = True

    def stop(self):
        self.running = False
        self.listening = False

    def start_conversation(self):
        self.conversation_mode = True
        print("Conversación iniciada")

    def end_conversation(self):
        self.conversation_mode = False
        print("Conversacion finalizada")