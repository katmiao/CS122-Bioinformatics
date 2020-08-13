import re

def bwt(text):
    matrix = []
    for i in range(0, len(text)):
        matrix.append(text[i:]+text[:i])
    matrix.sort()
    
    bwt = ""
    for i in range(0, len(matrix)):
        bwt += matrix[i][-1]

    print(bwt)

# input = "GCGTGCCTGGTCA$"
# bwt(input)

def inverseBWT(text):
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
    print("Last: " + str(last))

    first = last.copy()
    first.sort()
    print("First: " + str(first))

    genome = ["$1"]
    while len(genome) < len(first):
        sym = genome[-1]
        index = last.index(sym)
        genome.append(first[index])

    inverse = ""
    for i in range(1, len(genome)):
        inverse += genome[i][0]
    inverse += "$"
    print("Inverse: " + inverse)

# input = "TTCCTAACG$A"
# inverseBWT(input)

def getLastAndFirst(text):
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
    # print("Last: " + str(last))

    first = last.copy()
    first.sort()
    # print("First: " + str(first))

    return last, first

def generateLastToFirst(last, first):
    lastToFirst = []
    for i in last:
        lastToFirst.append(first.index(i))

    # print("lastToFirst: " + str(lastToFirst))

    return lastToFirst

def getRegexMatches(pattern, items):
    # print("pattern: "+pattern)
    # print("items: " +str(items))
    matches = []
    for i in range(0, len(items)):
        if re.search(pattern, items[i]):
            matches.append(i)
    return matches

def bwtMatching(lastCol, pattern, lastToFirst):
    top = 0
    bottom = len(lastCol) - 1
    # print("Top="+str(top)+", Bottom="+str(bottom))
    while top <= bottom:
        if len(pattern) > 0:
            sym = pattern.pop(-1)
            # print("sym: " + sym)
            subCol = lastCol[top:bottom+1]
            # print("subCol: " + str(subCol))
            matches = getRegexMatches("^"+sym, subCol)
            if len(matches) > 0:
                topIndex = top + matches[0]
                bottomIndex = top + matches[-1]
                
                top = lastToFirst[topIndex]
                bottom = lastToFirst[bottomIndex]
                # print("topIndex="+str(topIndex)+", bottomIndex="+str(bottomIndex))
                
            else:
                return  0
        else:
            return bottom - top + 1

def callBWTMatching():

    input = "TCCTCTATGAGATCCTATTCTATGAAACCTTCA$GACCAAAATTCTCCGGC"
    last, first = getLastAndFirst(input)
    lastToFirst = generateLastToFirst(last, first)
    patterns = ["CCT", "CAC", "GAG", "CAG", "ATC"]

    # patterns = []
    # readsfile = open('/Users/katmiao/Desktop/CS122/9.3/input.txt', 'r') 
    # patterns = readsfile.read().split()
    # readsfile.close() 

    matches = ""
    for pattern in patterns:
        matches += str(bwtMatching(last, list(pattern), lastToFirst)) + " "
    print(matches)

def generateCounts(firstCol, lastCol, lastToFirst):
    counts = {}
    for i in range(0,len(firstCol)+1):
        count = {"A":0, "C":0, "G":0, "T":0, "$":0}
        for j in range(0,i):
            count[lastCol[j][0]] += 1
        counts[i] = count

    return counts

def generateFirstOccurence(firstCol):
    occur = {"A":0, "C":0, "G":0, "T":0}
    
    for key in occur.keys():
        # print("key: "+key)
        # print(getRegexMatches("^"+key, firstCol))
        first = getRegexMatches("^"+key, firstCol)[0]
        occur[key] = first

    occur["$"] = 0
    return occur

def betterBWMatching(firstOccur, lastCol, pattern, counts):
    top = 0
    bottom = len(lastCol) - 1
    # print("top="+str(top)+", bottom="+str(bottom))
    while top <= bottom:

        if len(pattern) > 0:
            sym = pattern.pop(-1)
            # print("sym: " + sym)
            subCol = lastCol[top:bottom+1]
            # print("subCol: " + str(subCol))
            matches = getRegexMatches("^"+sym, subCol)
         
            if len(matches) > 0:
                
                top = firstOccur[sym] + counts[top][sym]
                bottom = firstOccur[sym] + counts[bottom+1][sym] - 1
                # print("topIndex="+str(topIndex)+", bottomIndex="+str(bottomIndex))
                
            else:
                return 0
        else:
            return bottom - top + 1


def callBetterBWT():
    # input = "GGCGCCGC$TAGTCACACACGCCGTA"
    patterns = ["ACC", "CCG", "CAG"]

    # patterns = []
    # readsfile = open('/Users/katmiao/Desktop/CS122/9.3/input.txt', 'r') 
    # patterns = readsfile.read().split()
    # readsfile.close() 


    last, first = getLastAndFirst(input)
    lastToFirst = generateLastToFirst(last, first)

    # print("FIRST: " +str(first))
    # print("LAST: " +str(last))
    # print("LASTTOFIRST: " +str(lastToFirst))

    counts = generateCounts(first, last, lastToFirst)
    firstOccur = generateFirstOccurence(first)

    # print("counts: " +str(counts))
    # print("firstOccur: " +str(firstOccur))

    matches = ""
    for pattern in patterns:
        matches += str(betterBWMatching(firstOccur, last, list(pattern), counts)) + " "
    print(matches)

    

callBetterBWT()