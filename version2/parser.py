import json
import re

class Parser:
    def __init__(self, wordlist_path):
        with open(wordlist_path, 'r') as f:
            data = json.load(f)
        self.verbs = set(data.get("verbs", []))
        self.objects = set(data.get("objects", []))
        self.prepositions = set(data.get("prepositions", []))
        self.patterns = [
            ("verb object", re.compile(rf"^({'|'.join(self.verbs)}) ({'|'.join(self.objects)})$")),
            ("verb object1 preposition object2", re.compile(
                rf"^({'|'.join(self.verbs)}) ({'|'.join(self.objects)}) ({'|'.join(self.prepositions)}) ({'|'.join(self.objects)})$")),
            ("verb", re.compile(rf"^({'|'.join(self.verbs)})$"))
        ]

    def classify(self, sentence):
        sentence = sentence.strip().lower()
        for label, pattern in self.patterns:
            if pattern.match(sentence):
                return label
        return "unknown sentence"

    def tokenize(self, sentence):
        return sentence.strip().lower().split()


    def add_pattern(self, label, regex):
        self.patterns.insert(0, (label, re.compile(regex)))

