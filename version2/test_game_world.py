from game_world import GameWorld

def test_game_world_initialization():
    world = GameWorld("world.json")
    for room_name in world.list_rooms():
        room = world.get_room(room_name)
        print(f"Room: {room_name}")
        print(room.describe())
        print("-" * 40)

if __name__ == "__main__":
    test_game_world_initialization()

