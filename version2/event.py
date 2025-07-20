class Event:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Event, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        pass  # Placeholder for any future initialization

    def check_for_events(self, obj1, obj2, verb, preposition):
        """
        Check if an event should be triggered based on the interaction between two GameObjects,
        a verb, and a preposition.

        Parameters:
        - obj1: GameObject
        - obj2: GameObject
        - verb: str
        - preposition: str
        """
        if verb in obj1.allowed_verbs and preposition in obj2.allowed_prepositions:
            print("Event generated")
        else:
            print("No event triggered")

