#https://medium.com/@info.gildacademy/a-simpler-way-to-implement-trie-data-structure-in-python-efa6a958a4f2
import random
class TrieNode():
    def __init__(self, nodeNum):
        self.children = {}
        self.terminating = False
        self.nodeNum = nodeNum

class Trie():
    def __init__(self):
        self.root = self.get_node()
        self.nodeCount = 0

    def get_node(self):
        return TrieNode(0)
    
    def insert(self, word):
        root = self.root
        wordLen = len(word)

        for i in range(wordLen):
            letter = word[i]

            if letter not in root.children.keys():
                self.nodeCount += 1
                root.children[letter] = TrieNode(self.nodeCount)
                # print("New node: " + letter + " at " + str(self.nodeCount))
            root = root.children.get(letter)
        
        # print("Inserted:"+word)

    def trieConstruction(self):
        root = self.root
        if not root:
            return 

        explore = [root]
        while(len(explore) > 0):
            node = explore[0]
            for child, childNode in node.children.items():
                print(str(node.nodeNum)+"->"+str(childNode.nodeNum)+":"+child)
                explore.append(childNode)
            explore.pop(0)

    def trieMatching(self, pattern):
        root = self.root
        if not root:
            return 

        matches = []
        explore = [root]
        while(len(explore) > 0):
            node = explore[0]
            # print("Trying " + str(node.nodeNum))
            for child, childNode in node.children.items():
                if child == pattern[0]:
                    # print("First match")
                    match = childNode
                    i = 1
                    while (i < len(pattern)):
                        if pattern[i] in match.children:
                            match = match.children[pattern[i]]
                            i += 1
                        else:
                            break
                    if (i == len(pattern)):
                        matches.append(childNode.nodeNum-1)
                explore.append(childNode)
            explore.pop(0)

        return matches

    def approxTrieMatching(self, pattern, d):
        root = self.root
        if not root:
            return 

        # print("\npattern: " +pattern)

        matches = []
        explore = [root]
        while(len(explore) > 0):
            node = explore[0]
            for child, childNode in node.children.items():
                mismatches = 0
                if child == pattern[0]:
                    mismatches = 0
                else: 
                    mismatches = 1

                match = childNode
                i = 1
                
                while (i < len(pattern) and mismatches <= d):
                    if pattern[i] in match.children:
                        match = match.children[pattern[i]]
                        i += 1
                    else:
                        mismatches += 1
                        if len(match.children) == 0:
                            continue
                        match = match.children[random.choice(list(match.children.keys()))]
                        i += 1

                if (i == len(pattern) and mismatches <= d):
                    matches.append(childNode.nodeNum-1)

                explore.append(childNode)
            explore.pop(0)

        return matches

# 9.3.4
# strings = ["ATAGA", "ATC", "GAT"]
# strings = []
# readsfile = open('/Users/katmiao/Desktop/CS122/9.3/input.txt', 'r') 
# strings = readsfile.read().splitlines()
# readsfile.close() 

# t = Trie()
# for genome in strings:
#     t.insert(genome)
# t.trieConstruction()

# 9.3.8
# genome = "ACATGCTACTTT"
# patterns = ["ATT","GCC","GCTA","TATT"]
# # patterns = []
# # readsfile = open('/Users/katmiao/Desktop/CS122/9.3/input.txt', 'r') 
# # patterns = readsfile.read().splitlines()
# # readsfile.close() 

# t = Trie()
# t.insert(genome)
# res = ""
# for pattern in patterns:
#     matches = t.approxTrieMatching(pattern, 1)
#     for m in matches:
#         res += str(m) + " "
# print(res)

# 9.14
dna = "ACATGCTACTTT"
patterns = ["ATT","GCC","GCTA","TATT"]
d=1

readfile = open('/Users/katmiao/Desktop/CS122/9.3/please.txt', 'r') 
dna, patterns, d = readfile.read().splitlines()
readfile.close() 
d = int(d)
patterns = patterns.split(' ')

t = Trie()
t.insert(dna)
res = ""
for pattern in patterns:
    matches = t.approxTrieMatching(pattern, d)
    for m in matches:
        res += str(m) + " "
print(res)