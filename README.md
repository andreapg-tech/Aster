# Aster ⭐

<p align="left">
  <b>English</b> | <a href="README.es.md">Leer en Español 🇪🇸</a>
</p>

**A voice assistant with an animated character and local AI models.** Aster listens, understands and talks back. Speech recognition, the LLM and speech synthesis all run on your own machine, so your voice and conversations never leave it; it only goes online to check the weather.

<!-- Once you have the GIF, save it as docs/demo.gif and uncomment the line below -->
<!-- ![Aster in action](docs/demo.gif) -->

## ✨ Features

- 🎙️ **Voice conversation** triggered by a wake word ("Aster").
- 🧠 **Local LLM** via Ollama (`qwen2.5:3b`): no API keys, and your conversations are never sent to the cloud.
- 🎯 **Intent detection** with the LLM: chatting, telling the time or date, and checking the weather.
- 🌦️ **Weather lookup** for any city through the [Open-Meteo](https://open-meteo.com) API (no API key needed).
- 📝 **Speech-to-text** with Faster-Whisper (`small` model on CPU) and **text-to-speech** with Piper TTS.
- 🔄 **State machine** that drives behaviour and animations.
- 🎭 **Animated character** built with Pygame-ce: blinking, gaze movements, falling asleep and waking up.
- ⏱️ **Inactivity handling**: goes back to sleep automatically.

> Aster currently speaks Spanish: the wake word, the voice model and the responses are in Spanish.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| UI and animation | Pygame-ce |
| Audio capture | SoundDevice |
| Speech-to-text | Faster-Whisper |
| LLM | Ollama (local models) |
| Text-to-speech | Piper TTS |
| Weather and geocoding | Open-Meteo API |

## 🔄 State Machine

```
SLEEPING ──(wake word)──► WAKE_UP ──► IDLE
                                       │
             ┌─────────────────────────┘
             ▼
         LISTENING ──► PROCESSING ──► SPEAKING ──► IDLE
                                                   │
                                             (inactivity)
                                                   ▼
                                               SLEEPING
```

| State | Description |
|---|---|
| `SLEEPING` | Asleep, eyes closed. |
| `WAKE_UP` | Gradually waking up. |
| `IDLE` | Waiting, blinking and looking around. |
| `LISTENING` | Listening to the user. |
| `PROCESSING` | Processing the input with the LLM. |
| `SPEAKING` | Answering out loud. |

## 🧠 Architecture

Responsibilities are split into independent modules:

```
src/
├── actions/      # Actions Aster can perform
├── aster/        # Core character logic
├── config/       # Configuration
├── core/         # Core components
├── events/       # System events
├── input/        # Audio capture and speech recognition
├── processing/   # Language and intent processing
├── render/       # Rendering and animations
├── services/     # Services (speech synthesis, weather, geocoding)
├── states/       # Aster and eye states
├── ui/           # Window and interface
└── main.py       # Entry point
```

## 📋 Requirements

- Python 3.11 or later
- [Ollama](https://ollama.com) installed and running
- Microphone and speakers
- Around 4 GB of free RAM for the local models (approximate)
- Internet connection only for weather lookups

## 🚀 Installation

**1. Clone the repository**
```bash
git clone https://github.com/andreapg-tech/Aster.git
cd Aster
```

**2. Create and activate a virtual environment**

Windows:
```bash
py -m venv .venv
.venv\Scripts\activate
```

Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install the dependencies**
```bash
pip install -r requirements.txt
```

**4. Download the language model**
```bash
ollama pull qwen2.5:3b
```

**5. Download the Piper voice**

Download `es_ES-davefx-medium.onnx` and `es_ES-davefx-medium.onnx.json` from [piper-voices](https://huggingface.co/rhasspy/piper-voices/tree/main/es/es_ES/davefx/medium). Save them in `models/piper/` at the project root, keeping their original names.

## ▶️ Usage

```bash
python src/main.py
```

Aster starts asleep. Say **"Aster"** (for example, "Hola, Aster") to wake it up and start talking. After a while without activity, it goes back to sleep.

Some things you can ask (in Spanish):

- "¿Qué hora es?" (What time is it?)
- "¿Qué día es hoy?" (What day is it today?)
- "¿Qué tiempo hará mañana en Madrid?" (What will the weather be like in Madrid tomorrow?)
- Or just chat with it.

## 🔮 Roadmap

- [ ] Memory across conversations
- [ ] More expressions and animations
- [ ] New actions and integrations
- [ ] A richer personality
- [ ] Porting the prototype to hardware

## 💡 What I Learned

Aster started as a personal project to bring together several areas of software development. Building it, I worked on:

- Designing a **modular architecture** and a **state machine**.
- Integrating a **complete voice pipeline** (STT → LLM → TTS) with local models.
- Coordinating the **animated interface** with audio processing.

## 👤 Author

**Andrea Pérez González** · [LinkedIn](https://www.linkedin.com/in/andreap%C3%A9rezgonz%C3%A1lez)
