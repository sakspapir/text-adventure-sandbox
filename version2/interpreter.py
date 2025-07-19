class Interpreter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Interpreter, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        pass  # No initialization needed for now

    def evaluate(self, sentence_structure, words, player):
        """
        sentence_structure: str - one of the recognized sentence types
        words: list - tokenized words from the sentence
        player: Player instance
        """
        room = player.get_current_room()
        inventory = player.inventory

        def find_object(name):
            for obj in room.objects + inventory:
                if obj.name == name:
                    return obj
            return None

        if sentence_structure == "verb object":
            verb, obj_name = words
            obj = find_object(obj_name)
            if obj and verb in obj.allowed_verbs:
                print("Event generated")
            else:
                print("Invalid action")

        elif sentence_structure == "verb object1 preposition object2":
            verb, obj1_name, prep, obj2_name = words
            obj1 = find_object(obj1_name)
            obj2 = find_object(obj2_name)
            if (obj1 and obj2 and
                verb in obj1.allowed_verbs and
                prep in obj2.allowed_prepositions):
                print("Event generated")
            else:
                print("Invalid action")

        elif sentence_structure == "verb":
            verb = words[0]
            print("Event generated")  # Assuming single verbs are always valid for now

        else:
            print("Unknown sentence structure")

