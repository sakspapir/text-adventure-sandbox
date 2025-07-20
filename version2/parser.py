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
        sentence = sentence.strip().lower()
        tokens = []
        words = sentence.split()
        i = 0

        # Combine all known tokens into a list with their type
        known_tokens = [(verb, 'verb') for verb in self.verbs] + \
                       [(obj, 'object') for obj in self.objects] + \
                       [(prep, 'preposition') for prep in self.prepositions]

        # Sort known tokens by length (descending) to match longest first
        known_tokens.sort(key=lambda x: len(x[0].split()), reverse=True)

        while i < len(words):
            matched = False
            for token, _ in known_tokens:
                token_words = token.split()
                if words[i:i+len(token_words)] == token_words:
                    tokens.append(token)
                    i += len(token_words)
                    matched = True
                    break
            if not matched:
                tokens.append(words[i])
                i += 1

        return tokens

    def add_pattern(self, label, regex):
        self.patterns.insert(0, (label, re.compile(regex)))

