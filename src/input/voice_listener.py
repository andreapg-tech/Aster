import threading


class VoiceListener:

    def __init__(self, voice_input, event_queue):
        self.voice_input = voice_input
        self.event_queue = event_queue
        self.running = False
        self.thread = None

    def start(self):
        self.running = True

        self.thread = threading.Thread(
            target=self._listen_loop,
            daemon=True
        )

        self.thread.start()

    def _listen_loop(self):
        while self.running:
            text = self.voice_input.listen()

            if self.voice_input.contains_wake_word(text):
                print("¡Wake word detectada!")
                self.event_queue.put("WAKE_UP")

    def stop(self):
        self.running = False