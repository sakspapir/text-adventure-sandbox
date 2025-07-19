class Player:
    def __init__(self):
        self.inventory = []

class GameContext:
    def __init__(self, current_room=None, player=None):
        self.current_room = current_room
        self.player = player

game_context = GameContext()

