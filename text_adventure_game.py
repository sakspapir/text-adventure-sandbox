import re

# -----------------------------
# Synonym Registry
# -----------------------------
class SynonymRegistry:
    def __init__(self):
        self.synonyms = {}

    def register(self, canonical, *aliases):
        canonical = canonical.lower()
        self.synonyms[canonical] = canonical
        for alias in aliases:
            self.synonyms[alias.lower()] = canonical

    def normalize(self, phrase):
        words = phrase.lower().split()
        normalized = [self.synonyms.get(word, word) for word in words]
        return ' '.join(normalized)

# -----------------------------
# Game Entities
# -----------------------------
class Item:
    def __init__(self, name, description='', synonyms=None):
        self.name = name.lower()
        self.description = description
        self.synonyms = synonyms or []
        self.picked_up = False

    def matches(self, name, synonym_registry):
        return synonym_registry.normalize(name) == synonym_registry.normalize(self.name)

class Room:
    def __init__(self, name, description=''):
        self.name = name
        self.description = description
        self.items = []
        self.exits = {}
        self.state = {}

    def describe(self):
        desc = self.description + "\n"
        visible_items = [item.name for item in self.items if not item.picked_up]
        if visible_items:
            desc += "You see: " + ", ".join(visible_items)
        else:
            desc += "There is nothing of interest here."
        return desc

# -----------------------------
# Player and Context
# -----------------------------
class Player:
    def __init__(self):
        self.inventory = []

class GameContext:
    def __init__(self, current_room, player):
        self.current_room = current_room
        self.player = player

# -----------------------------
# Event System
# -----------------------------
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

# -----------------------------
# Game Engine
# -----------------------------
class GameEngine:
    def __init__(self):
        self.synonyms = SynonymRegistry()
        self.rooms = {}
        self.player = Player()
        self.current_room = None
        self.events = []

    def add_room(self, room):
        self.rooms[room.name] = room
        if not self.current_room:
            self.current_room = room

    def add_event(self, event):
        self.events.append(event)

    def register_synonyms(self):
        self.synonyms.register("pick up", "take", "acquire")
        self.synonyms.register("look at", "inspect", "examine")
        self.synonyms.register("use", "activate")
        self.synonyms.register("go", "walk", "move")
        self.synonyms.register("stone", "rock", "pebble")
        self.synonyms.register("dirty old spoon", "rusty spoon")
        self.synonyms.register("door", "wooden door", "old door")

    def find_item(self, name):
        for item in self.current_room.items + self.player.inventory:
            if item.matches(name, self.synonyms):
                return item
        return None

    def process_command(self, command):
        command = command.lower().strip()
        command = self.synonyms.normalize(command)

        if command == "look":
            return self.current_room.describe()

        match = re.match(r"(pick up) (.+)", command)
        if match:
            _, item_name = match.groups()
            item = self.find_item(item_name)
            if item and not item.picked_up:
                item.picked_up = True
                self.player.inventory.append(item)
                return f"You picked up the {item.name}."
            return f"You can't pick up {item_name}."

        match = re.match(r"(look at) (.+)", command)
        if match:
            _, item_name = match.groups()
            item = self.find_item(item_name)
            if item:
                return f"You look at the {item.name}. {item.description}"
            return f"You don't see a {item_name} here."

        match = re.match(r"(use) (.+) on (.+)", command)
        if match:
            _, item_name, target_name = match.groups()
            item = self.find_item(item_name)
            target = self.find_item(target_name)
            if item and target:
                return f"You use the {item.name} on the {target.name}."
            return "That doesn't seem to work."

        match = re.match(r"(go) (.+)", command)
        if match:
            _, exit_name = match.groups()
            exit_name = self.synonyms.normalize(exit_name)
            if exit_name in self.current_room.exits:
                self.current_room = self.current_room.exits[exit_name]
                return self.current_room.describe()
            return "You can't go that way."

        return "I don't understand that command."

    def check_events(self):
        context = GameContext(self.current_room, self.player)
        for event in self.events:
            if event.check(context):
                print(f"[Event Triggered] {event.name}")

    def run(self):
        print(self.current_room.describe())
        while True:
            try:
                command = input("\n> ")
            except EOFError:
                print("\nExiting game.")
                break
            if command.lower() in ["quit", "exit"]:
                print("Goodbye!")
                break
            response = self.process_command(command)
            print(response)
            self.check_events()

# -----------------------------
# Game Setup
# -----------------------------
def setup_game():
    engine = GameEngine()
    engine.register_synonyms()

    room1 = Room("mysterious room", "You are in a mysterious room with a door, a computer, and a book shelf.")
    room2 = Room("hallway", "You are in a dimly lit hallway. There is a staircase leading up.")
    room1.exits["door"] = room2

    stone = Item("stone", "A small round stone.", synonyms=["rock", "pebble"])
    spoon = Item("dirty old spoon", "A rusty spoon with dried food on it.", synonyms=["rusty spoon"])
    key = Item("key", "A small brass key.")

    room1.items.extend([stone, spoon, key])

    engine.add_room(room1)
    engine.add_room(room2)

    event = Event(
        "Unlock Door Event",
        lambda ctx: any(item.name == "key" and item.picked_up for item in ctx.player.inventory),
        lambda ctx: ctx.current_room.name == "hallway"
    )
    engine.add_event(event)

    return engine

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    game = setup_game()
    game.run()
