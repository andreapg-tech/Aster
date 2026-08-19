import pygame
import threading
import io
import wave
from pathlib import Path
from piper import PiperVoice

class SpeechService:

    def __init__(self):
        self.model_path = Path("models/piper/es_ES-davefx-medium.onnx")
        self.voice = PiperVoice.load(str(self.model_path))
        self.speaking = False

    def speak(self, text):
        if self.speaking:
            return
        
        thread = threading.Thread(
            target=self._speak,
            args=(text,),
            daemon=True
        )
        thread.start()

    def _speak(self, text):
        self.speaking = True

        try:
            audio_buffer = io.BytesIO()

            with wave.open(audio_buffer, "wb") as wav_file:
                self.voice.synthesize_wav(
                    text,
                    wav_file
                )

            audio_buffer.seek(0)

            pygame.mixer.music.load(
                audio_buffer,
                "response.wav"
            )

            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except pygame.error as e:
            print(f"Error reproduciendo audio: {e}")

        finally:
            self.speaking = False

    def is_speaking(self):
        return self.speaking