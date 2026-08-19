# Aster ⭐

Aster es un asistente virtual interactivo desarrollado en Python.

El proyecto combina una interfaz animada, interacción por voz, procesamiento de lenguaje y síntesis de voz para crear un personaje interactivo capaz de escuchar, procesar y responder al usuario.

## ✨ Características

- 🎭 Personaje animado mediante Pygame.
- 👀 Parpadeos y movimientos de mirada.
- 😴 Estados de sueño y despertar.
- 🎙️ Interacción mediante voz.
- 🧠 Procesamiento de intenciones.
- 🔊 Respuestas mediante síntesis de voz.
- 💬 Modo de conversación.
- 🔄 Máquina de estados para controlar el comportamiento del personaje.
- ⏱️ Gestión automática del estado de inactividad.

## 🧠 Arquitectura

Aster está organizado en diferentes componentes para separar la lógica del personaje, la interfaz, la entrada de voz, el procesamiento y los servicios.

```text
src/
├── actions/       # Acciones que Aster puede ejecutar
├── aster/         # Lógica principal del personaje
├── config/        # Configuración del proyecto
├── core/          # Componentes centrales
├── events/        # Eventos del sistema
├── input/         # Entrada y reconocimiento de voz
├── processing/    # Procesamiento del lenguaje 
|                    e intenciones
├── render/        # Renderizado y animaciones
├── services/      # Servicios utilizados por
|                    la aplicación
├── states/        # Estados de Aster y sus ojos
├── ui/            # Ventana e interfaz
└── main.py        # Punto de entrada
```

## 🔄 Máquina de estados

El comportamiento de Aster se controla mediante una máquina de estados.

```text
                    ┌───────────┐
                    │ SLEEPING  │
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
                    │ SPEAKING  │───────────────┘
                    └───────────┘
                          │
                          │ Inactivity
                          ▼
                    ┌───────────┐
                    │ SLEEPING  │
                    └───────────┘
```

Cada estado controla el comportamiento y las animaciones que muestra el personaje.

## 🛠️ Tecnologías

- **Python** — lenguaje principal del proyecto.
- **Pygame-ce** — renderizado de la interfaz y animaciones.
- **SoundDevice** — captura de audio mediante el micrófono.
- **SpeechRecognition** — gestión de la entrada de voz.
- **Faster-Whisper** — transcripción de voz a texto.
- **Piper TTS** — síntesis de voz.
- **Ollama** — procesamiento de lenguaje mediante modelos locales.
- **Git / GitHub** — control de versiones y gestión del proyecto.

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/andreapg-tech/Aster.git
cd Aster
```

### 2. Crear un entorno virtual

En Windows:

```bash
py -m venv .venv
```

### 3. Activar el entorno virtual

```bash
.venv\Scripts\activate
```

### 4. Instalar las dependencias

```bash
py -m pip install -r requirements.txt
```

## ▶️ Ejecución

Con el entorno virtual activado:

```bash
py src/main.py
```

Aster iniciará en estado de sueño y podrá despertarse mediante la interacción por voz.

## 🎙️ Interacción

El flujo principal de interacción es:

```text
Aster dormido
      │
      ▼
Reconocimiento de la palabra de activación
      │
      ▼
Despertar
      │
      ▼
Escuchar
      │
      ▼
Procesar la entrada
      │
      ▼
Responder mediante voz
      │
      ▼
Continuar la conversación
      │
      ▼
Inactividad
      │
      ▼
Volver a dormir
```

## 🎨 Estados visuales

Aster cuenta actualmente con diferentes estados para representar su comportamiento:

| Estado | Descripción |
|---|---|
| `SLEEPING` | Aster está dormido con los ojos cerrados. |
| `WAKE_UP` | Aster se despierta progresivamente. |
| `IDLE` | Estado de espera, con parpadeos y movimientos de mirada. |
| `LISTENING` | Aster está escuchando al usuario. |
| `PROCESSING` | Aster está procesando la entrada recibida. |
| `SPEAKING` | Aster está generando una respuesta hablada. |

## 📁 Organización del proyecto

El proyecto utiliza una arquitectura modular para separar responsabilidades.

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

## 🔮 Próximas mejoras

Algunas posibles líneas de evolución del proyecto son:

- 🧠 Sistema de memoria.
- 🎭 Mayor variedad de expresiones y animaciones.
- 💡 Nuevas acciones e integraciones.
- 🤖 Personalidad más desarrollada.
- 🖥️ Mejoras de la interfaz.
- 🔌 Migración del prototipo a hardware.

## 🎯 Objetivo del proyecto

Aster comenzó como un proyecto personal para explorar el desarrollo de un personaje interactivo y combinar diferentes áreas del desarrollo de software.

El proyecto permite trabajar con:

- Programación en Python.
- Arquitectura modular.
- Máquinas de estados.
- Procesamiento de voz.
- Procesamiento de lenguaje.
- Síntesis de voz.
- Animación e interfaces.
- Integración de diferentes componentes.

## 👤 Autor

Proyecto personal desarrollado como parte de mi aprendizaje y portfolio de Ingeniería Informática.