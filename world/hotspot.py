class Hotspot:
    def __init__(self, name, description=''):
        self.name = name
        self.description = description

    def matches(self, name, synonym_registry):
        return synonym_registry.normalize(name) == synonym_registry.normalize(self.name)
