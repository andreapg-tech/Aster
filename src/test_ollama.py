import ollama


response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": """
Devuelve únicamente JSON.

Clasifica la intención de este texto:

"Hola Aster, ¿me puedes decir qué hora tenemos?"

Intenciones posibles:
- get_current_time
- unknown

Formato obligatorio:
{"intent": "...", "parameters": {}}
"""
        }
    ]
)

print(response["message"]["content"])