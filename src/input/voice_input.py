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

        self.voice_threshold = 0.01

    def listen(self, max_duration=15, silence_duration=1.5):
        print("Escuchando...")

        chunk_duration = 0.1
        chunk_size = int(self.sample_rate * chunk_duration)

        pre_buffer_duration = 0.3
        pre_buffer_size = int(pre_buffer_duration / chunk_duration)

        pre_buffer = []

        audio_chunks = []

        recording = False
        silence_time = 0.0
        elapsed_time = 0.0

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            blocksize=chunk_size
        )as stream:
            while elapsed_time < max_duration:
                audio, _ = stream.read(chunk_size)
                audio = audio.copy()
                elapsed_time += chunk_duration

                pre_buffer.append(audio)

                if len(pre_buffer) > pre_buffer_size:
                    pre_buffer.pop(0)

                if self.is_voice(audio):
                    if not recording:
                        print("Voz detectada...")
                        recording = True

                        audio_chunks.extend(pre_buffer)
                        silence_time = 0.0

                    else:
                        audio_chunks.append(audio)
                        silence_time = 0.0

                elif recording:
                    audio_chunks.append(audio)

                    silence_time += chunk_duration

                    if silence_time >=silence_duration:
                        break

        if not audio_chunks:
            return ""

        print("Procesando...")

        audio = np.concatenate(audio_chunks, axis=0)

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
            initial_prompt="Hola Aster.",
            vad_filter=True,
            vad_parameters=dict(
                min_silence_duration_ms=1000
            )
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        print(f"Texto detectado: '{text}'")

        os.remove(temp_file.name)

        return text

    def contains_wake_word(self, text):
        return "aster" in text.lower()

    def is_voice(self, audio):
        volume = np.sqrt(np.mean(audio ** 2))
        print(f"RMS: {volume:.4f} | Umbral: {self.voice_threshold:.4f}")
        return volume > self.voice_threshold

    def calibrate_noise(self, duration=2):
        print("Calibrando micrófono...")
        print("Por favor, permanece en silencio.")

        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        noise_level = np.sqrt(np.mean(audio ** 2))

        self.voice_threshold = noise_level * 2.5

        print(f"Nivel de ruido: {noise_level:.4f}")
        print(f"Umbral de voz: {self.voice_threshold:.4f}")