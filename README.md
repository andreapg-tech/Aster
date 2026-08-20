# Aster ⭐

<p align="left">
  <b>English</b> | <a href="README.es.md">Leer en Español 🇪🇸</a>
</p>

Aster is an interactive virtual assistant developed in Python.

The project combines an animated interface, voice interaction, local language processing, and speech synthesis to create an interactive character capable of listening, processing, and responding to the user.

## ✨ Features

- 🎭 Animated character using Pygame-ce.
- 👀 Blinking and gaze movements.
- 😴 Sleeping and waking states.
- 🎙️ Voice-controlled interaction.
- 🧠 Local intent processing.
- 🔊 Speech synthesis (TTS) responses.
- 💬 Continuous conversation mode.
- 🔄 State machine to control character behavior.
- ⏱️ Automatic inactivity management.

## 🧠 Architecture

Aster is structured into modular components to separate the character logic, visual interface, audio capturing, processing, and external services.

```text
src/
├── actions/       # Actions Aster can execute
├── aster/         # Core character logic
├── config/        # Project settings and configurations
├── core/          # App orchestration and event loop
├── events/        # System events definitions
├── input/         # Audio capture and speech recognition
├── processing/    # Language processing and
                     intent classification
├── render/        # Eye rendering and animations
├── services/      # Geolocation, weather, and
                     TTS services
├── states/        # State definitions (Aster and Eyes)
├── ui/            # Pygame window setup
└── main.py        # Entry point
```

## 🔄 State Machine

Aster's behavior is controlled by a state machine.

```text
                    ┌───────────┐
                    │  SLEEPING │
                    └─────┬─────┘
                          │
                       Wake Up
                          │
                          ▼
                    ┌───────────┐
                    │  WAKE_UP  │
                    └─────┬─────┘
                          │
                          ▼
                    ┌───────────┐
                    │   IDLE    │◄──────────────┐
                    └─────┬─────┘               │
                          │                     │
                    Wake / Voice                │
                          │                     │
                          ▼                     │
                    ┌───────────┐               │
                    │ LISTENING │               │
                    └─────┬─────┘               │
                          │                     │
                          ▼                     │
                    ┌───────────┐               │
                    │PROCESSING │               │
                    └─────┬─────┘               │
                          │                     │
                          ▼                     │
                    ┌───────────┐               │
                    │  SPEAKING │───────────────┘
                    └───────────┘
                          │
                          │ Inactivity
                          ▼
                    ┌───────────┐
                    │  SLEEPING │
                    └───────────┘
```

Each state controls the character's behavior and the animations displayed on the screen.

## 🛠️ Technologies

- **Python** — Core language.
- **Pygame-ce** — Interface rendering and animations.
- **SoundDevice** — Live microphone audio capture.
- **SpeechRecognition** — Audio stream helper.
- **Faster-Whisper** — Local, fast speech-to-text transcription.
- **Piper TTS** — Local, fast text-to-speech synthesis.
- **Ollama** — Local LLM integration (using `qwen2.5:3b`).
- **Git / GitHub** — Version control.

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/andreapg-tech/Aster.git
cd Aster
```

### 2. Create a virtual environment
On Windows:
```bash
py -m venv .venv
```

### 3. Activate the virtual environment
```bash
.venv\Scripts\activate
```

### 4. Install dependencies
```bash
py -m pip install -r requirements.txt
```

### 5. Configure Ollama
Ensure you have [Ollama](https://ollama.com/) installed and running. Then, pull the required local LLM:
```bash
ollama run qwen2.5:3b
```

### 6. Download the Piper voice model
Create a directory named `models/piper/` in the root of the project. Download both the voice model and its JSON configuration, and save them in that folder:
- [es_ES-davefx-medium.onnx](https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx)
- [es_ES-davefx-medium.onnx.json](https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json)

*Make sure the files are named exactly `es_ES-davefx-medium.onnx` and `es_ES-davefx-medium.onnx.json` inside `models/piper/`.*

## ▶️ Execution

With the virtual environment activated:
```bash
py src/main.py
```

Aster will start in a sleeping state and will wake up when it hears the wake word.

## 🎙️ Interaction

The main interaction flow is:

```text
Aster is sleeping
      │
      ▼
Activation word recognition ("Aster")
      │
      ▼
Wake up (Animation)
      │
      ▼
Listen to user input
      │
      ▼
Process input with Ollama
      │
      ▼
Respond using voice (Piper TTS)
      │
      ▼
Continue conversation
      │
      ▼
Inactivity Timeout
      │
      ▼
Go back to sleep
```

## 🎨 Visual States

Aster currently has different states to represent its behavior:

| State | Description |
|---|---|
| `SLEEPING` | Aster is sleeping with its eyes closed. |
| `WAKE_UP` | Aster opens its eyes progressively. |
| `IDLE` | Default waiting state with random blinking and looking around. |
| `LISTENING` | Aster is actively listening to the user. |
| `PROCESSING` | Aster is processing the input. |
| `SPEAKING` | Aster is generating a spoken response. |

## 📁 Project Organization

The project uses a modular architecture to separate responsibilities.

```text
Aster/
│
├── src/
│   ├── actions/
│   ├── aster/
│   ├── config/
│   ├── core/
│   ├── events/
│   ├── input/
│   ├── processing/
│   ├── render/
│   ├── services/
│   ├── states/
│   ├── ui/
│   └── main.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## 🔮 Future Enhancements

Some possible paths for the project's evolution are:

- 🧠 Long-term memory system.
- 🎭 Greater variety of eye expressions and animations.
- 💡 More actions and API integrations.
- 🤖 Developed conversational personality.
- 🖥️ UI refinements.
- 🔌 Hardware porting (running Aster on a physical screen/Raspberry Pi).

## 🎯 Project Goal

Aster started as a personal project to explore the development of an interactive character and combine different areas of software development.

The project allows working with:

- Python programming.
- Modular architecture.
- State machines.
- Speech processing.
- Language processing.
- Speech synthesis.
- Animations and interfaces.
- Component integration.

## 👤 Author

Personal project built as part of my learning journey and portfolio for Computer Engineering.
