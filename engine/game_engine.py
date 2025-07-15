import re
from world.synonyms import SynonymRegistry
from world.item import Item
from world.room import Room
from engine.context import GameContext, Player
from engine.event import Event

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
