from processing.intent import Intent
from actions.action_handler import ActionHandler


handler = ActionHandler()

intent = Intent("get_current_time")

result = handler.execute(intent)

print("Resultado:", result)