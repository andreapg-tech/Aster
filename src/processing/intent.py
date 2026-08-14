class Intent:

    def __init__(self, name, parameters=None):
        self.name = name
        self.parameters = parameters or {}