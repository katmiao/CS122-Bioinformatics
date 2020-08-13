import random
from itertools import product
import re

# You can use both BWT and smith-waterman
# 1. for 1 read. let's say kind of long (100 bp)
# 2. split this read into smaller fragments. (say 10 bp each)
# 		10 fragments each of size 10 bp. 
# 3. you see where each read may match to reference genome, 
# 		--> BWT + FM index (on a fragment len 10 bp). 
# 		--> you do BWT + FM total of 10 times (10 fragments)
# 		--> if 2nd fragment matches the reference, 
# 		--> then you have the other 90 bp that didn't match
# 		--> your "new input" is from position 
# 					0-9 and 20-99 
# 4. for the rest of the read (which is the other 90 bp)
# 		--> don't want to use hamming distance 
# 		--> smith-waterman to handle indel. 
# 				--> may be do it on edited genome


def divide(dna, d):
    """ Divide a string into small pieces so that at least one fragment is free of errors. d is the number of errors"""
    length = len(dna)
    l = length // (d+1)
    k = length % (d+1) ## higher d will split patterns into shorter length
    result = []
    i = 0
    while i < length: ## not very important just doing some splitting
        if k > 0:
            result.append((dna[i:i+l+1], i))
            k -= 1
            i += l+1
        else:
            result.append((dna[i:i+l], i))
            i += l
    return result

def HammingDistance(s1, s2): ##! can use anything else, but Hamming is very fast and easy
    if len(s1) != len(s2): return float('inf')
    return sum(1 if s1[i] != s2[i] else 0 for i in range(len(s1)))

class BWT():
    def __init__(self, dna):
        self.last, self.first = self.getLastAndFirst(dna)
        self.lastToFirst = self.generateLastToFirst(self.last, self.first)
        self.counts = self.generateCounts(self.first, self.last, self.lastToFirst)
        self.firstOccur = self.generateFirstOccurence(self.first)

    def getLastAndFirst(self, text):
        counts1 = {"A":0, "C":0, "G":0, "T":0, "$":0}
        counts2 = {"A":0, "C":0, "G":0, "T":0, "$":0}
        last = []
        for t in text:
            counts1[t] += 1
        for i in range(0, len(text)):
            sym = text[i]
            counts2[sym] += 1
            zeros = (len(str(counts1[sym])) - len(str(counts2[sym]))) * "0"
            last.append(sym+zeros+str(counts2[sym]))
        first = last.copy()
        first.sort()
        return last, first

    def generateLastToFirst(self, last, first):
        lastToFirst = []
        for i in last:
            lastToFirst.append(first.index(i))
        return lastToFirst

    def getRegexMatches(self, pattern, items):
        matches = []
        for i in range(0, len(items)):
            if re.search(pattern, items[i]):
                matches.append(i)
        return matches

    def generateCounts(self, firstCol, lastCol, lastToFirst):
        counts = {}
        for i in range(0,len(firstCol)+1):
            count = {"A":0, "C":0, "G":0, "T":0, "$":0}
            for j in range(0,i):
                count[lastCol[j][0]] += 1
            counts[i] = count
        return counts

    def generateFirstOccurence(self, firstCol):
        occur = {"A":0, "C":0, "G":0, "T":0}
        for key in occur.keys():
            first = self.getRegexMatches("^"+key, firstCol)[0]
            occur[key] = first
        occur["$"] = 0
        return occur

    def betterBWMatching(self, pattern):
        top = 0
        bottom = len(self.last) - 1
        print("top="+str(top)+", bottom="+str(bottom))
        res = []
        while top <= bottom:
            if len(pattern) > 0:
                sym = pattern.pop(-1)
                print("sym: " + sym)
                subCol = self.last[top:bottom+1]
                print("subCol: " + str(subCol))
                matches = self.getRegexMatches("^"+sym, subCol)
            
                if len(matches) > 0:
                    top = self.firstOccur[sym] + self.counts[top][sym]
                    bottom = self.firstOccur[sym] + self.counts[bottom+1][sym] - 1
                else:
                    return 0
            else:
                res.append(bottom - top + 1)
        return res

def APM(pattern, d, Text, B, counts, firstOccur):
    """ Approximate Pattern Matching """
    result = set()
    l = len(pattern)
    fragments = divide(pattern, d) ## pattern => read
    for f in fragments: ## each fragment of each pattern
        print("fragment: "+str(f))
        s, i = f ## get the sequence, and the index where it occurs in the read
        rest = pattern[:i] + pattern[i+len(s):] ## get the rest of pattern (note fragment came from pattern)... maybe we can speed this up...
        print("rest: "+rest)
        fmIndexing = [B.betterBWMatching(list(s))]
        for p in fmIndexing:
        # for p in B.lookup(s): ##! use BWT to look where this small fragment of pattern match. note that B.lookup is just doing FM indexing, change it into your own function
            ##! note: @p should be an interger saying where the match is found, can match at many places
            target = Text[p-i:p] + Text[p+len(s):p-i+l] ## get the text that match. the reference genome sourrounding location p.
            if HammingDistance(rest, target) <= d: ## keep results if we have only "a few" errors.
                result.add(p-i)
    return result

def solve(): ##! assume some input: long-string, patterns-to-match, some-error-rate
    result = []
    readfile = open('/Users/katmiao/Desktop/CS122/9.3/input.txt', 'r') 
    dna, patterns, d = readfile.read().splitlines()
    readfile.close() 
    d = int(d)
    patterns = patterns.split(' ')
    B = BWT(dna) ##! you need to implement the BWT or take it from https://nbviewer.jupyter.org/github/BenLangmead/comp-genomics-class/blob/master/notebooks/CG_FmIndex.ipynb

    for p in patterns:
        for i in APM(p, d, dna, B, B.counts, B.firstOccur):
            result.append(i)
    return ' '.join(sorted(map(str, result)))


solve()