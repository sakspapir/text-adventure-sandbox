import re
from world.synonyms import SynonymRegistry
from world.item import Item
from world.room import Room
from engine.context import game_context, Player
from engine.event import Event

class GameEngine:
    def __init__(self):
        self.synonyms = SynonymRegistry()
        self.rooms = {}
        self.events = []

    def add_room(self, room):
        self.rooms[room.name] = room
        if not game_context.current_room:
            game_context.current_room = room

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
        for item in game_context.current_room.items + game_context.player.inventory + game_context.current_room.hotspots:
            if item.matches(name, self.synonyms):
                return item
        return None

    def process_command(self, command):
        command = command.lower().strip()
        command = self.synonyms.normalize(command)

        if command == "look":
            return game_context.current_room.describe()

        match = re.match(r"(pick up) (.+)", command)
        if match:
            _, item_name = match.groups()
            item = self.find_item(item_name)
            if not hasattr(item,"picked_up"):
                return f"You can't pick up {item_name}"
            if item and not item.picked_up:
                item.picked_up = True
                game_context.player.inventory.append(item)
                return f"You picked up the {item.name}."
            return f"You can't pick up {item_name}."

        match = re.match(r"(look at) (.+)", command)
        if match:
            _, item_name = match.groups()
            item = self.find_item(item_name)
            if item:
                return f"You look at the {item.name}. {item.description}"
            return f"You don't see a {item_name} here."

        matchUseOn = re.match(r"(use) (.+) on (.+)", command)
        if matchUseOn:
            _, item_name, target_name = matchUseOn.groups()
            item = self.find_item(item_name)
            target = self.find_item(target_name)
            if item and target:
                # Try triggering events with item and target
                for event in self.events:
                    if event.check(type="use item on target",item=item, target=target):
                        return f"You use the {item.name} on the {target.name}."

                return "That doesn't seem to work."
            else:
                return "item or target = None"

        matchUse = re.match(r"(use) (.+)", command)
        if matchUse and not matchUseOn:
            _, item_name = matchUse.groups()
            item = self.find_item(item_name)
            if item:
                # Try triggering events with item and target
                for event in self.events:
                    if event.check(type="use item",item=item):
                        return f"You use the {item.name}."

                return "That doesn't seem to work."
            else:
                return "item = None"

        match = re.match(r"(go) (.+)", command)
        if match:
            _, exit_name = match.groups()
            exit_name = self.synonyms.normalize(exit_name)
            matched_object = next((exit for exit in game_context.current_room.exits if exit.name == exit_name), None)
            desc = matched_object.describe()
            if matched_object.passable == True:
                game_context.current_room = matched_object.toRoom
                desc += "\n\n" + game_context.current_room.describe()
            return desc

        return "I don't understand that command."

    def check_events(self):
        for event in self.events:
            if event.check():
                print(f"[Event Triggered] {event.name}")

    def run(self):
        print(game_context.current_room.describe())
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
            #self.check_events()
