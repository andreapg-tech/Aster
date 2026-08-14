import json
import ollama

from processing.intent import Intent
from processing.intents import INTENTS


class LanguageProcessor:

    def __init__(self):
        self.model = "qwen2.5:3b"

    def process(self, text):

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": f"""
                Eres el procesador de lenguaje de Aster.

                Tu trabajo es interpretar lo que dice el usuario
                y convertirlo en una intención.

                Intenciones disponibles:
                {", ".join(INTENTS)}

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

                Si ninguna intención coincide, utiliza "unknown".

                No respondas al usuario.
                No expliques nada.
                Solo devuelve JSON.
                """
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        content = response["message"]["content"]

        try:
            data = json.loads(content)

            intent_name = data["intent"]

            if intent_name not in INTENTS:
                return Intent("unknown")

            return Intent(
                intent_name,
                data.get("parameters", {})
            )

        except (json.JSONDecodeError, KeyError):
            return Intent("unknown")