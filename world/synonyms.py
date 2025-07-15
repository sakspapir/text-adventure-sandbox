class SynonymRegistry:
    def __init__(self):
        self.synonyms = {}

    def register(self, canonical, *aliases):
        canonical = canonical.lower()
        self.synonyms[canonical] = canonical
        for alias in aliases:
            self.synonyms[alias.lower()] = canonical

    def normalize(self, phrase):
        words = phrase.lower().split()
        normalized = [self.synonyms.get(word, word) for word in words]
        return ' '.join(normalized)
