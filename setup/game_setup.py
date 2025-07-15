from engine.game_engine import GameEngine
from engine.event import Event
from world.room import Room
from world.item import Item

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
