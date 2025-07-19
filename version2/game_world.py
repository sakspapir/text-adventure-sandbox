from room import Room
from object import GameObject
import json

class GameWorld:
    _instance = None

    def __new__(cls, config_path="world.json"):
        if cls._instance is None:
            cls._instance = super(GameWorld, cls).__new__(cls)
            cls._instance._initialize(config_path)
        return cls._instance

    def _initialize(self, config_path):
        with open(config_path, 'r') as f:
            data = json.load(f)

        self.rooms = {}
        for room_data in data.get("rooms", []):
            room = Room(room_data["name"], room_data["description"])
            for obj_data in room_data.get("objects", []):
                obj = GameObject(
                    name=obj_data["name"],
                    allowed_verbs=obj_data.get("allowed_verbs", []),
                    allowed_prepositions=obj_data.get("allowed_prepositions", []),
                    can_be_picked_up=obj_data.get("can_be_picked_up", False),
                    state=obj_data.get("state", "")
                )
                room.add_object(obj)
            self.rooms[room.name] = room

    def get_room(self, name):
        return self.rooms.get(name)

    def list_rooms(self):
        return list(self.rooms.keys())

