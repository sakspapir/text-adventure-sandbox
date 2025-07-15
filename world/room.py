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
