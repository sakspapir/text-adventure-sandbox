from engine.context import game_context


class Event:
    def __init__(self, name,oneTimeEvent, *conditions, actions=None):
        self.name = name
        self.oneTimeEvent = oneTimeEvent
        self.conditions = conditions
        self.triggered = False
        self.actions = actions

    def check(self, **kwargs):
        if self.oneTimeEvent:
            if self.triggered:
                return False
        result = all(cond(game_context, **kwargs) for cond in self.conditions)
        if result:
            self.triggered = True
            for action in self.actions:
                action(game_context, **kwargs)
        return result

