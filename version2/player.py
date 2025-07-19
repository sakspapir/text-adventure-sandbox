class Player:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Player, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.current_room = None
        self.inventory = []

    def set_current_room(self, room):
        self.current_room = room

    def get_current_room(self):
        return self.current_room

    def add_to_inventory(self, obj):
        self.inventory.append(obj)

    def remove_from_inventory(self, obj_name):
        self.inventory = [obj for obj in self.inventory if obj.name != obj_name]

    def list_inventory(self):
        return [obj.name for obj in self.inventory]

