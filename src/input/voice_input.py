import os
import tempfile

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel


class VoiceInput:

    def __init__(self):
        self.sample_rate = 44100

        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    def listen(self, duration=5):
        print("Escuchando...")

        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        print("Procesando...")

        audio_int16 = np.int16(audio * 32767)

        temp_file = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        temp_file.close()

        write(
            temp_file.name,
            self.sample_rate,
            audio_int16
        )

        segments, _ = self.model.transcribe(
            temp_file.name,
            language="es",
            initial_prompt="Hola Aster."
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        os.remove(temp_file.name)

        return text

    def contains_wake_word(self, text):
        return "aster" in text.lower()