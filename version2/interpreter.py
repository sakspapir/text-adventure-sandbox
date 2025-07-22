from event import Event
from player import protagonist

class Interpreter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Interpreter, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.event_handler = Event()

    def evaluate(self, sentence_structure, words):
        room = protagonist.get_current_room()
        inventory = protagonist.inventory

        def find_object(name):
            for obj in room.objects + inventory:
                if obj.name == name:
                    return obj
            return None

        if sentence_structure == "verb object":
            verb, obj_name = words
            obj = find_object(obj_name)
            if obj and verb in obj.allowed_verbs:
                self.event_handler.check_for_events(obj, obj, verb, "", sentence_structure)
            else:
                print("Invalid action")

        elif sentence_structure == "verb object1 preposition object2":
            verb, obj1_name, prep, obj2_name = words
            obj1 = find_object(obj1_name)
            obj2 = find_object(obj2_name)
            if (obj1 and obj2 and
                verb in obj1.allowed_verbs and
                prep in obj2.allowed_prepositions):
                self.event_handler.check_for_events(obj1, obj2, verb, prep, sentence_structure)
            else:
                print("Invalid action")

        elif sentence_structure == "verb":
            verb = words[0]
            #print("Event generated")  # Placeholder for verb-only events

        else:
            print("Unknown sentence structure")

