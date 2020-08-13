import random

class Trie():
    def __init__(self):
        self.root = {"num" : 0, "next" : {}, "val" : ""}
        self.nodeCount = 0

    def getRoot(self):
        return self.root

    def printTrie(self):
        print(self.root)

    def printEdges(self):
        explore = [self.root]
        while(len(explore) > 0):
            node = explore[0]
            print(node["val"])
            for child, childNode in node["next"].items():
                explore.append(childNode)
            explore.pop(0)
    
    def insert(self, word):
        root = self.root
        wordLen = len(word)

        for i in range(wordLen):
            letter = word[i]

            if letter not in root["next"].keys():
                self.nodeCount += 1
                root["next"][letter] = {"next":{}, "num":self.nodeCount, "val":letter}
                # print("New node: " + letter + " at " + str(self.nodeCount))
            root = root["next"].get(letter)
        
        # print("Inserted:"+word)

    def trieConstruction(self):
        root = self.root
        if not root:
            return 

        explore = [root]
        while(len(explore) > 0):
            node = explore[0]
            for child, childNode in node["next"].items():
                print(str(node["num"])+"->"+str(childNode["num"])+":"+child)
                explore.append(childNode)
            explore.pop(0)

    def trieMatching(self, pattern):
        root = self.root
        if not root:
            return 

        matches = ""
        explore = [root]
        while(len(explore) > 0):
            node = explore[0]
            for child, childNode in node["next"].items():
                if child == pattern[0]:
                    match = childNode
                    i = 1
                    while (i < len(pattern)):
                        if pattern[i] in match["next"]:
                            match = match["next"][pattern[i]]
                            i += 1
                        else:
                            break
                    if (i == len(pattern)):
                        matches += str(childNode["num"]-1) + " "
                explore.append(childNode)
            explore.pop(0)

        print(matches)

    def recurseBranch(self, root):
        # print("\nrecurseBranch: " + str(root))
        if not root:
            return []

        if len(root["next"]) == 0:
            return [root["val"]]

        # if not root or len(root["next"]) == 0:
        #     return []

        branches = []
        # print("at root: "+root["val"])

        for child, childNode in root["next"].items():
            childBranches = self.recurseBranch(childNode)
            # print("at child: "+childNode["val"])
            # print("got branches: "+str(childBranches))
            
            for branch in childBranches:
                branches.append(root["val"]+branch)

        
        return branches

    def longestRepeat(self):
        repeats = self.root.copy()
        explore = [repeats]

        while(len(explore) > 0):
            node = explore[0]
            popMe = []
            # print("Node: " + node["val"])
            for child, childNode in node["next"].items():
                if len(childNode["next"]) <= 0:
                    popMe.append(child)
                else:
                    explore.append(childNode)

            for p in popMe:
                # print("Popping: " + node["next"][p]["val"])
                node["next"].pop(p)

            explore.pop(0)

        # print("Repeats: " + str(repeats))

        longest = ""
        branches = self.recurseBranch(repeats)
        print("\nBRANCHES: " + str(branches))
        for b in branches:
            if len(b) > len(longest):
                longest = b
        print("\nLongest: " + longest)

    def oldcondense(self):
        root = self.root
        if not root:
            return

        explore = [root]
        while(len(explore) > 0):
            node = explore[0]
            
            if len(node["next"]) == 1:
                # key1, val1 = node["next"].popitem()
                key1, val1 = random.choice(list(node["next"].items()))
                if len(val1["next"]) == 1:
                    key2, val2 = val1["next"].popitem()
                    node["next"] = {key1+key2: val2}
                 
            for child, childNode in node["next"].items():
                explore.append(childNode)

            explore.pop(0)

        print("\n\n\nDONE CONDENSING (old). \nRoot: "+str(self.root))

    def condense(self):
        root = self.root
        if not root:
            return

        explore = []
        children = [root]
        while(len(children) > 0):
            node = children.pop(0)
            explore.append(node)
            for child, childNode in node["next"].items():
                children.append(childNode)

        while (len(explore) > 0):
            node = explore.pop(-1)
            
            if len(node["next"]) == 1:
                key, val = node["next"].popitem()
                node["val"] = node["val"] + val["val"]
                node["next"] = val["next"]
                # print("Condensing: " + str(node))
                        

# ==============================================================================

def suffixTreeConstruction():
    # text = "ATAAATG$"
    text = "ATATCGTTTTATCGTT"
    t = Trie()
    for i in range(0, len(text)):
        t.insert(text[i:])
    t.oldcondense()
    t.printTrie()
    t.printEdges()
# suffixTreeConstruction()

def longestRepeatProblem():
    text = "ATATCGTTTTATCGTT$"
    t = Trie()
    for i in range(0, len(text)):
        t.insert(text[i:])

    t.condense()
    # t.printTrie()
    t.longestRepeat()

# longestRepeatProblem()

def longestSharedSubstring():
    text1 = "TCGGTAGATTGCGCCCACTC"
    text2 = "AGGGGCTCGCAGTGTAAGAA"

    trie1 = Trie()
    for i in range(0, len(text1)):
        trie1.insert(text1[i:])
    trie2 = Trie()
    for i in range(0, len(text2)):
        trie2.insert(text2[i:])

    root1 = trie1.getRoot()
    root2 = trie2.getRoot()

    longest = ""
    explore = [("", root1)]
    while (len(explore) > 0):
        substr, node1 = explore.pop(0)
        node2 = root2

        for i in range(0, len(substr)):
            node2 = node2["next"][substr[i]]

        for child, childNode in node1["next"].items():
            if child in node2["next"].keys():
                explore.append((substr+child, childNode))
            else:
                if len(substr) > len(longest):
                    longest = substr
                    print("new longest: " + longest)
    print("Longest: " + str(longest))

# longestSharedSubstring()

def shortedNonSharedSubstring():
    text1 = "CCAAGCTGCTAGAGG"
    text2 = "CATGCTGGGCTGGCT"

    trie1 = Trie()
    for i in range(0, len(text1)):
        trie1.insert(text1[i:])
    trie2 = Trie()
    for i in range(0, len(text2)):
        trie2.insert(text2[i:])

    root1 = trie1.getRoot()
    root2 = trie2.getRoot()

    shortest = text1
    explore = [("", root1)]
    while (len(explore) > 0):
        substr, node1 = explore.pop(0)
        node2 = root2

        for i in range(0, len(substr)):
            node2 = node2["next"][substr[i]]

        for child, childNode in node1["next"].items():
            if child in node2["next"].keys():
                explore.append((substr+child, childNode))
            else:
                if len(substr) + 1 < len(shortest):
                    shortest = substr+child
                    print("new shortest: " + shortest)
    print("shortest: " + str(shortest))

# shortedNonSharedSubstring()

def suffixArray():
    text = "AACGATAGCGGTAGA$"

    suffixes = []
    for i in range(0, len(text)):
        suffixes.append((text[i:], i))
    
    sortedSuffixes = sorted(suffixes, key=lambda x:x[0])
    print("sorted: " + str(sortedSuffixes))
    res = ""
    for s in sortedSuffixes:
        res += str(s[1]) + ", "

    print(res)

suffixArray()