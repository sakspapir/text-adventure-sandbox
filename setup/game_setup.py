from engine.game_engine import GameEngine
from engine.event import Event
from world.room import Room
from world.item import Item
from world.hotspot import Hotspot
from world.room import Exit
from engine.context import game_context, Player

def log_condition(name, func):
    def wrapper(ctx, **kwargs):
        result = func(ctx, **kwargs)
        print(f"[Condition: {name}] -> {result}")
        return result
    return wrapper

def setup_game():
    engine = GameEngine()
    engine.register_synonyms()

    room1 = Room("mysterious room", "You are in a mysterious room with a door, a computer, and a book shelf.")
    room2 = Room("hallway", "You are in a dimly lit hallway. There is a staircase leading up.")
    room1_door_exit = Exit("door",room1,room2,False, "You open the door and walk through it.", "The door is locked.")
    room1.exits.extend([room1_door_exit])
    room3 = Room("Computer screen", "The computer screen is black except for the words:\n\n  \"say rewind\"\n\n...in big, white letters in the middle of the screen...\n(You can leave the computer by typing \"go back\")")
    room3_exit = Exit("back",room3,room1,True)
    room3.exits.extend([room3_exit])

    stone = Item("stone", "A small round stone.", synonyms=["rock", "pebble"])
    spoon = Item("dirty old spoon", "A rusty spoon with dried food on it.", synonyms=["rusty spoon"])
    key = Item("key", "A small brass key.")

    room1_door = Hotspot("door", "A big, sturdy door")

    room1_computer = Hotspot("computer", "A dusty, old computer. Probably from the early nineties.")
    room1_bookshelf = Hotspot("book shelf", "The book shelf is filled with books.")

    room1.items.extend([stone, spoon, key])
    room1.hotspots.extend([room1_door, room1_computer, room1_bookshelf])

    engine.add_room(room1)
    engine.add_room(room2)

    player = Player()
    game_context.player = player
    game_context.current_room = room1

    event = Event(
        "Unlock Door Event",
        True, #oneTimeEvent: trigger only once
        log_condition("Has key", lambda ctx, **kwargs: any(item.name == "key" and item.picked_up for item in ctx.player.inventory)),
        log_condition("In room1", lambda ctx, **kwargs: ctx.current_room == room1),
        log_condition("Using key on door", lambda ctx, **kwargs: kwargs.get("item") and kwargs.get("target") and kwargs["item"].name == "key" and kwargs["target"].name == "door"),
        log_condition("use item on target", lambda ctx, **kwargs: kwargs.get("type") and kwargs["type"] == "use item on target"),
        actions=[lambda ctx, **kwargs: setattr(room1_door_exit, "passable", True) or print("You hear a click. The door is now unlocked.")]
    )
    engine.add_event(event)
    event = Event(
        "Use computer Event",
        False, #triggers multiple times
        log_condition("In room1", lambda ctx, **kwargs: ctx.current_room == room1),
        log_condition("use computer", lambda ctx, **kwargs: kwargs.get("item") and kwargs["item"].name == "computer"),
        log_condition("use item", lambda ctx, **kwargs: kwargs.get("type") and kwargs["type"] == "use item"), 
        actions=[lambda ctx, **kwargs: setattr(game_context, "current_room", room3) or print("You turn on the computer. For some reason, you know the login password...")]
    )
    engine.add_event(event)

    return engine
