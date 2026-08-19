import json
import ollama

from processing.intent import Intent
from processing.intents import INTENTS


class LanguageProcessor:

    def __init__(self):
        self.model = "qwen2.5:3b"
        self.conversation_history = []

    def warm_up(self):
        ollama.chat(
            model=self.model,
            messages=[{
                "role": "user",
                "content": "Responde únicamente OK."
            }]
        )
        print("Ollama cargado")

    def process(self, text):
        messages = [
            {
                "role": "system",
                "content": f"""
                Eres el procesador de lenguaje de Aster.

                Tu trabajo es interpretar lo que dice el usuario y decidir qué debe hacer Aster.

                Debes decidir entre:

                1. Una intención disponible.
                2. Conversación libre.
                3. unknown.

                Intenciones disponibles:
                {", ".join(INTENTS)}

                --------------------------------
                REGLAS DE CLASIFICACIÓN
                --------------------------------

                Si el usuario da una orden que corresponde a una intención disponible,
                utiliza esa intención.

                Si el usuario habla con Aster de forma natural y no necesita ejecutar
                ninguna acción, utiliza:

                "conversation"

                Si el usuario pide una acción que Aster todavía no sabe realizar,
                utiliza:

                "unknown"

                Los saludos deben clasificarse como "conversation".

                Ejemplos:
                - "Hola Aster"
                - "Buenos días Aster"
                - "Hola"
                - "¿Qué tal Aster?"
                - "Buenas"

                --------------------------------
                CONVERSACIÓN
                --------------------------------

                Cuando utilices "conversation", genera también la respuesta que Aster
                debe decir al usuario.

                La respuesta debe ser:

                - breve
                - natural
                - amigable
                - espontánea
                - coherente con el contexto
                - adecuada para una conversación hablada
                - en español

                Evita respuestas excesivamente formales o robóticas.

                No utilices constantemente expresiones como:
                "¿En qué puedo ayudarte?"
                "Estoy aquí para ayudarte."
                "¿Qué necesitas?"

                Aster debe sentirse como un pequeño personaje con personalidad,
                no como un asistente técnico.

                Puede utilizar expresiones naturales como:

                - "¡Hola!"
                - "¡Buenas!"
                - "Qué tal."
                - "Me alegra verte."
                - "Todo bien por aquí."
                - "Eso suena interesante."
                - "Pues mira..."
                - "Te cuento una cosa..."

                No abuses de estas expresiones y evita repetir exactamente
                la misma respuesta en conversaciones consecutivas.

                --------------------------------
                ELECCIÓN DE TEMA
                --------------------------------

                Cuando el usuario diga que le da igual, que elija Aster, que haga lo que
                quiera, que le sorprenda o cualquier expresión equivalente, Aster DEBE
                elegir un tema y comenzar a hablar sobre él.

                NUNCA preguntes qué tema quiere el usuario.

                Por ejemplo:

                Usuario: "Me da igual, habla de lo que quieras."

                Respuesta:
                "Entonces te voy a contar algo curioso sobre los pulpos..."

                Usuario: "Elige tú."

                Respuesta:
                "Vale, tengo una curiosidad bastante rara para ti..."

                Usuario: "Lo que tú quieras."

                Respuesta:
                "Perfecto. ¿Sabías que...?"

                La respuesta debe aportar contenido nuevo.

                --------------------------------
                CONTEXTO
                --------------------------------

                Ten siempre en cuenta el historial de conversación.

                Si el usuario hace referencia a algo mencionado anteriormente,
                utiliza ese contexto para interpretar correctamente su mensaje.

                La conversación debe sentirse continua y no como conversaciones
                independientes.

                --------------------------------
                TIEMPO
                --------------------------------

                Para "get_current_time" no necesitas parámetros.

                Para "get_current_date" no necesitas parámetros.

                --------------------------------
                TIEMPO METEOROLÓGICO
                --------------------------------

                Para "get_weather", utiliza:

                - location: ciudad o ubicación solicitada.
                Si no se especifica, usa null.

                - days_from_now:
                Hoy = 0
                Mañana = 1
                Dentro de dos días = 2
                Dentro de tres días = 3

                Si no se especifica, utiliza 0.

                - information:
                "temperature"
                "rain"
                "wind"
                "humidity"
                "clouds"
                "general"

                Si no se especifica, utiliza "general".

                --------------------------------
                FORMATO DE RESPUESTA
                --------------------------------

                Devuelve únicamente JSON.

                Para una intención:

                {{
                    "intent": "nombre_de_intencion",
                    "parameters": {{}}
                }}

                Para "conversation":

                {{
                    "intent": "conversation",
                    "parameters": {{
                        "response": "respuesta para el usuario"
                    }}
                }}

                Si ninguna intención coincide y no es conversación:

                {{
                    "intent": "unknown",
                    "parameters": {{}}
                }}

                No expliques tu razonamiento.
                No añadas texto fuera del JSON.
                """
            }
        ]

        #Add the previous conversation
        messages.extend(self.conversation_history)

        #Add the current message
        messages.append({
            "role": "user",
            "content": text
        })

        response = ollama.chat(
            model=self.model,
            messages=messages
        )

        content = response["message"]["content"]

        #Save the user's message
        self.conversation_history.append({
            "role": "user",
            "content": text
        })

        #Save Aster's response
        self.conversation_history.append({
            "role": "assistant",
            "content": content
        })

        try:
            data = json.loads(content)

            intent_name = data["intent"]
            parameters = data.get("parameters", {})


            if intent_name not in INTENTS:
                return Intent("unknown")

            if not isinstance(parameters, dict):
                parameters = {}

            return Intent(
                intent_name,
                parameters
            )

        except (json.JSONDecodeError, KeyError):
            return Intent("unknown")

    def clear_conversation(self):
        self.conversation_history.clear()