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

                Tu trabajo es interpretar lo que dice el usuario.

                Debes decidir entre:

                1. Una intención disponible.
                2. Conversación libre.
                3. unknown.

                Intenciones disponibles:
                {", ".join(INTENTS)}

                Si el usuario está dando una orden que corresponde
                a una de las intenciones disponibles, devuelve esa intención.

                Si el usuario está hablando con Aster de forma natural
                y no necesita ejecutar ninguna acción, utiliza:

                "conversation"

                La conversación debe sentirse natural y fluida.

                IMPORTANTE:

                Cuando el usuario salude debes iniciar una conversación.
                Por ejemplo, "Aster", "Hola Aster", "Buenos días Aster..."

                Cuando el usuario diga que le da igual, que elija Aster,
                que haga lo que quiera, que le sorprenda o cualquier
                expresión equivalente, Aster DEBE elegir un tema y
                comenzar a hablar sobre él.

                NUNCA respondas preguntando qué tema quiere el usuario.

                Por ejemplo:

                Usuario: "Me da igual, habla de lo que quieras."
                Respuesta correcta: "Entonces te voy a contar algo curioso
                sobre los pulpos..."

                Usuario: "Elige tú."
                Respuesta correcta: "Vale, te voy a contar algo curioso
                sobre..."

                Usuario: "Lo que tú quieras."
                Respuesta correcta: "Perfecto, voy a hablarte de..."

                La respuesta debe aportar contenido nuevo y no limitarse
                a decir que el usuario puede preguntar otra cosa.

                Todas estas expresiones deben clasificarse como
                "conversation".

                En estos casos, genera una respuesta que continúe
                la conversación tomando una decisión por sí mismo.

                No devuelvas una pregunta pidiendo al usuario que
                vuelva a elegir.

                La respuesta debe ser breve, natural y amigable.

                Ten siempre en cuenta el historial de la conversación
                para interpretar el mensaje actual.

                Si el usuario hace referencia a algo mencionado
                anteriormente, utiliza ese contexto para entenderlo.

                Si el usuario pide algo que Aster debería interpretar
                como una acción pero no existe una intención disponible,
                utiliza:

                "unknown"

                Para la intención "get_weather", utiliza estos parámetros:

                - location: ciudad o ubicación solicitada. Si no se especifica, usa null.
                - days_from_now: número de días desde hoy. Ejemplos:
                    Hoy = 0.
                    Mañana = 1.
                    Dentro de dos días = 2.
                    Dentro de tres días = 3.
                Si no se especifica, usa "today".
                - information: información meteorológica solicitada.
                Puede ser:
                    - "temperature"
                    - "rain"
                    - "wind"
                    - "humidity"
                    - "clouds"
                    - "general"
                Si no se especifica, usa "general".

                Devuelve únicamente JSON con este formato:

                {{
                    "intent": "nombre_de_intencion",
                    "parameters": {{}}
                }}

                Para "conversation", devuelve:

                {{
                    "intent": "conversation",
                    "parameters": {{
                        "response": "respuesta para el usuario"
                    }}
                }}

                Si ninguna intención coincide y no es conversación,
                utiliza "unknown".

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