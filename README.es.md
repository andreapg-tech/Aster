# Aster ⭐

<p align="left">
  <a href="README.md">Read in English 🇬🇧</a> | <b>Español</b>
</p>

**Asistente de voz con personaje animado y modelos de IA locales.** Aster escucha, entiende y responde hablando. La transcripción, el LLM y la síntesis de voz se ejecutan en tu equipo, así que tu voz y tus conversaciones no salen de él; solo se conecta a internet para consultar el tiempo.

<p align="center">
  <img src="docs/demo.gif" alt="Aster se despierta, mira a su alrededor, parpadea y vuelve a dormirse" width="480">
</p>

## ✨ Características

- 🎙️ **Conversación por voz** con palabra de activación ("Aster").
- 🧠 **LLM local** con Ollama (`qwen2.5:3b`): sin API keys y sin enviar tus conversaciones a la nube.
- 🎯 **Detección de intenciones** con el LLM: conversar, decir la hora o la fecha y consultar el tiempo.
- 🌦️ **Consulta del tiempo** de cualquier ciudad con la API de [Open-Meteo](https://open-meteo.com) (sin API key).
- 📝 **Transcripción** con Faster-Whisper (modelo `small` en CPU) y **síntesis de voz** con Piper TTS.
- 🔄 **Máquina de estados** que controla el comportamiento y las animaciones.
- 🎭 **Personaje animado** con Pygame-ce: parpadeos, movimientos de mirada, dormir y despertar.
- ⏱️ **Gestión de inactividad**: vuelve a dormirse automáticamente.

## 🛠️ Tecnologías

| Componente | Tecnología |
|---|---|
| Lenguaje | Python |
| Interfaz y animación | Pygame-ce |
| Captura de audio | SoundDevice |
| Voz a texto | Faster-Whisper |
| LLM | Ollama (modelos locales) |
| Texto a voz | Piper TTS |
| Tiempo y geolocalización | API de Open-Meteo |

## 🔄 Máquina de estados

```
SLEEPING ──(palabra de activación)──► WAKE_UP ──► IDLE
                                                   │
             ┌─────────────────────────────────────┘
             ▼
         LISTENING ──► PROCESSING ──► SPEAKING ──► IDLE
                                                   │
                                          (inactividad)
                                                   ▼
                                               SLEEPING
```

| Estado | Descripción |
|---|---|
| `SLEEPING` | Dormido, con los ojos cerrados. |
| `WAKE_UP` | Se despierta poco a poco. |
| `IDLE` | En espera, con parpadeos y movimientos de mirada. |
| `LISTENING` | Escuchando al usuario. |
| `PROCESSING` | Procesando la entrada con el LLM. |
| `SPEAKING` | Respondiendo por voz. |

## 🧠 Arquitectura

El proyecto separa responsabilidades en módulos independientes:

```
src/
├── actions/      # Acciones que Aster puede ejecutar
├── aster/        # Lógica principal del personaje
├── config/       # Configuración
├── core/         # Componentes centrales
├── events/       # Eventos del sistema
├── input/        # Captura y reconocimiento de voz
├── processing/   # Procesamiento del lenguaje e intenciones
├── render/       # Renderizado y animaciones
├── services/     # Servicios (síntesis de voz, tiempo, geolocalización)
├── states/       # Estados de Aster y de sus ojos
├── ui/           # Ventana e interfaz
└── main.py       # Punto de entrada
```

## 📋 Requisitos

- Python 3.11 o superior
- [Ollama](https://ollama.com) instalado y en ejecución
- Micrófono y altavoces
- Unos 4 GB de RAM libres para los modelos locales (orientativo)
- Conexión a internet solo para consultar el tiempo

## 🚀 Instalación

**1. Clona el repositorio**
```bash
git clone https://github.com/andreapg-tech/Aster.git
cd Aster
```

**2. Crea y activa un entorno virtual**

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

**3. Instala las dependencias**
```bash
pip install -r requirements.txt
```

**4. Descarga el modelo de lenguaje**
```bash
ollama pull qwen2.5:3b
```

**5. Descarga la voz de Piper**

Descarga `es_ES-davefx-medium.onnx` y `es_ES-davefx-medium.onnx.json` desde [piper-voices](https://huggingface.co/rhasspy/piper-voices/tree/main/es/es_ES/davefx/medium). Guárdalos en `models/piper/`, en la raíz del proyecto, sin cambiarles el nombre.

## ▶️ Uso

```bash
python src/main.py
```

Aster empieza dormido. Di **"Aster"** (por ejemplo, "Hola, Aster") para despertarlo y empezar a hablar con él. Si no hay actividad durante un rato, vuelve a dormirse.

Algunas cosas que puedes pedirle:

- "¿Qué hora es?"
- "¿Qué día es hoy?"
- "¿Qué tiempo hará mañana en Madrid?"
- O simplemente charlar con él.

## 🔮 Próximas mejoras

- [ ] Sistema de memoria entre conversaciones
- [ ] Más expresiones y animaciones
- [ ] Nuevas acciones e integraciones
- [ ] Personalidad más desarrollada
- [ ] Migración del prototipo a hardware

## 💡 Qué he aprendido

Aster empezó como un proyecto personal para combinar varias áreas del desarrollo de software. Con él he trabajado:

- El diseño de una **arquitectura modular** y de una **máquina de estados**.
- La integración de un **pipeline de voz completo** (STT → LLM → TTS) con modelos locales.
- La coordinación entre la **interfaz animada** y el procesamiento de audio.

## 👤 Autora

**Andrea Pérez González** · [LinkedIn](https://www.linkedin.com/in/andreap%C3%A9rezgonz%C3%A1lez)
