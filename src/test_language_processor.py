from processing.language_processor import LanguageProcessor


processor = LanguageProcessor()

tests = [
    "¿Qué hora es?",
    "Hola Aster, ¿qué hora es?",
    "¿Qué tiempo hace?",
    "Hola Aster"
]

for text in tests:
    intent = processor.process(text)

    print(f"Texto: {text}")
    print(f"Intent: {intent.name}")
    print(f"Parámetros: {intent.parameters}")
    print()