from parser import Parser

# Instantiate the parser with the word list JSON file
parser = Parser("words.json")

# Define a list of test sentences
test_sentences = [
    "eat apple",
    "move box to door",
    "open",
    "run fast",
    "open box with apple",
    "eat door on box",
    "take box with apple",
    "pick up apple",
    "walk to door",
    "pick up tiny little spoon with old chair"
]

# Run each test sentence through the parser and print the result
for sentence in test_sentences:
    result = parser.classify(sentence)
    print(f"'{sentence}' => {result}")

