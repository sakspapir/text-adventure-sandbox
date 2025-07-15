class Event:
    def __init__(self, name, *conditions):
        self.name = name
        self.conditions = conditions
        self.triggered = False

    def check(self, context):
        if self.triggered:
            return False
        result = all(cond(context) for cond in self.conditions)
        if result:
            self.triggered = True
        return result
