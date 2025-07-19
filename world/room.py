class Room:
    def __init__(self, name, description=''):
        self.name = name
        self.description = description
        self.items = []
        self.hotspots = []
        self.exits = []
        self.state = {}

    def describe(self):
        desc = self.description + "\n"
        visible_items = [item.name for item in self.items if not item.picked_up]
        if visible_items:
            desc += "You see: " + ", ".join(visible_items)
        else:
            desc += "There is nothing of interest here."
        return desc

class Exit:
    def __init__(self,name, fromRoom, toRoom, passable=True, open_text="", closed_text=""):
        self.passable = passable
        self.fromRoom = fromRoom
        self.toRoom = toRoom
        self.name = name
        self.open_text = open_text
        self.closed_text = closed_text
        
    def describe(self):
        if self.passable:
            return self.open_text
        else:
            return self.closed_text
