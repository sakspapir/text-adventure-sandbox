class Item:
    def __init__(self, name, description='', synonyms=None):
        self.name = name.lower()
        self.description = description
        self.synonyms = synonyms or []
        self.picked_up = False

    def matches(self, name, synonym_registry):
        return synonym_registry.normalize(name) == synonym_registry.normalize(self.name)
