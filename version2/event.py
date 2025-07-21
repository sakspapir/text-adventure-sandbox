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

    def check_for_events(self, obj1, obj2, verb, preposition):
        unlock_door_in_entrance_hall(obj1,obj2,verb,preposition)



# EVENT FUNCTIONS

def unlock_door_in_entrance_hall(obj1, obj2, verb, preposition):
    if protagonist.get_current_room().name != "Entrance Hall":
        return
    if obj1.name == "key" and obj2.name == "door" and verb == "use" and preposition == "with":
        if protagonist.is_in_inventory(obj1) == False:
            print("You don't have a key")
            return
        if obj2.state == "locked":
            obj2.state = "closed"
            print("The door is now unlocked.")
        else:
            print("The door is not locked.")

