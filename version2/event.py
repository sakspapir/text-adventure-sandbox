from player import protagonist

class Event:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Event, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        pass        

    def check_for_events(self, obj1, obj2, verb, preposition, sentence_structure):
        unlock_door_in_entrance_hall(obj1,obj2,verb,preposition,sentence_structure)
        if sentence_structure == "verb object":
            pick_up_item(obj1,obj2,verb,"")


# EVENT FUNCTIONS

def unlock_door_in_entrance_hall(obj1, obj2, verb, preposition, sentence_structure):
    if protagonist.get_current_room().name != "Entrance Hall":
        return
    if obj1.name == "key" and obj2.name == "door" and verb == "use" and (preposition == "with" or preposition == "on"):
        if protagonist.is_in_inventory(obj1) == False:
            print("You don't have a key")
            return
        if obj2.state == "locked":
            obj2.state = "closed"
            print("The door is now unlocked.")
        else:
            print("The door is not locked.")

def pick_up_item(obj1,obj2,verb,preposition):
    if obj1.can_be_picked_up:
        if obj1 in protagonist.get_current_room().objects:
            protagonist.get_current_room().remove_object(obj1.name)
            protagonist.add_to_inventory(obj1)
            print(f"You picked up {obj1.name}")
        else:
            print(f"There is now {obj1.name} here.")
