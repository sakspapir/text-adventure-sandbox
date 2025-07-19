class GameObject:
    def __init__(self, name, allowed_verbs=None, allowed_prepositions=None, can_be_picked_up=False, state=""):
        self.name = name
        self.allowed_verbs = allowed_verbs if allowed_verbs else []
        self.allowed_prepositions = allowed_prepositions if allowed_prepositions else []
        self.can_be_picked_up = can_be_picked_up
        self.state = state

    def display_status(self):
        status = (
            f"Object Name: {self.name}\n"
            f"Allowed Verbs: {', '.join(self.allowed_verbs)}\n"
            f"Allowed Prepositions: {', '.join(self.allowed_prepositions)}\n"
            f"Can be picked up: {'Yes' if self.can_be_picked_up else 'No'}\n"
            f"Current State: {self.state}"
        )
        return status

