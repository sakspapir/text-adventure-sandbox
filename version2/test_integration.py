import json
import re
from game_world import GameWorld
from player import Player
from parser import Parser
from object import GameObject
from room import Room
from interpreter import Interpreter

# Load word list from words.json
with open("words.json", "r") as f:
    wordlist = json.load(f)

# Instantiate singletons
world = GameWorld("world.json")
player = Player()
parser = Parser("words.json")
interpreter = Interpreter()

# Set player in starting room
starting_room = world.get_room("Entrance Hall")
player.set_current_room(starting_room)

# Test sentences
sentences = [
    "open door",
    "pick key",
    "use key with door",
    "read book",
    "turn on lamp",
    "fly away"
]

for sentence in sentences:
    structure = parser.classify(sentence)
    tokens = parser.tokenize(sentence)
    print(f"Sentence: '{sentence}' => Structure: {structure}")
    interpreter.evaluate(structure, tokens, player)
    print("-" * 40)

