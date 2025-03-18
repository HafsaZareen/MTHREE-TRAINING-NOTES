# dictionary_db = {
#     "apple": "A fruit",
#     "car": "A vehicle",
#     "python": "A programming language",
#     "book": "A set of written pages",
#     "computer": "An electronic device"
# }

# def search_word(word):
#     if word in dictionary_db: 
#         return f"{word}: {dictionary_db[word]}"
#     else:
#         return f"{word} not found in dictionary."

# print(search_word("apple"))    
# print(search_word("python"))   
# print(search_word("banana"))

import time

# Trie Node Definition
class TrieNode:
    def __init__(self):
        self.children = {}  # Dictionary of characters
        self.is_end_of_word = False  # Marks the end of a word

#  Trie Data Structure
class Trie:
    def __init__(self):
        self.root = TrieNode()

    # Insert a word into the Trie
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True  # Marks the complete word

    # 🔍 Search for a word in the Trie
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word  # True if it's a full word in Trie

#  Load words from file into Trie
def load_words(filename, trie):
    with open(filename, "r") as file:
        for line in file:
            trie.insert(line.strip().lower())  # Convert to lowercase for consistency

# Measure search time
def search_word(trie, word):
    word = word.lower()
    start_time = time.time()  # Start time
    found = trie.search(word)  # Trie lookup O(m)
    end_time = time.time()  # End time

    if found:
        print(f"\n Word Found: {word}")
    else:
        print(f"\nWord Not Found: {word}")
    
    print(f" Time Taken: {(end_time - start_time):.6f} seconds\n")

#  Create Trie & Load Words
trie = Trie()
load_words("/mnt/d/mthree/notes/week5/words.txt", trie)

# Search for words
search_word(trie, "python")  # Existing word


