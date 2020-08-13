import random

# PART 1 - parse file
paths = {}
readsfile = open('/Users/katmiao/Desktop/CS122/db.txt', 'r') 
# genome = readsfile.read().splitlines()
while True:
    line = readsfile.readline()
    if not line:
        break
    splitkey = line.split(" -> ")
    key = splitkey[0]
    vals = splitkey[1].strip("\n")
    splitvals = vals.split(",")
    paths[key] = splitvals
readsfile.close() 

# PART 2 - find the startnode and find cycles
rempaths = paths.copy()
cycles = {}         # key: startnode, val: cycle in list
node = random.choice(list(rempaths))
# node = "0"
next = []
unexplored = set()
startnode = node
cycle = []

while len(rempaths) != 0:
    # print("Node: " + node)
    cycle.append(node)
    if node in rempaths.keys():
        next = rempaths.pop(node)
        # print("Next: " + str(next))
        if len(next) == 1:
            unexplored.discard(node)
            node = next[0]
        elif len(next) > 1:
            rempaths[node] = next[1:]
            unexplored.add(node)
            node = next[0]
    else:
        # end of a cycle, pick another starting point
        unexplored.discard(node)
        # print("REMPATHS: " + str(rempaths))
        # print("UNEXPLORED: " + str(unexplored))

        # log cycle
        cycles[node] = cycle
        cycle = []

        if len(unexplored) > 0:
            node = unexplored.pop()
            # print("hmm")
            # unexplored = set()
        else:
            # print("lol tf")
            node = next[0]
            break

if len(rempaths) == 0:
    cycle.append(node)
    cycles[node] = cycle

# print("Startnode: " + node)
# print("CYCLES: " + str(cycles))

# PART 3 - we have the starting node! find path

def getkey(val, d):
    for key, vals in d.items():
        if val in vals:
            return key
    return None

def makeECycle(startnode, cycles):
    ecycle = str(startnode)
    # print("StartNode: " + startnode)
    # print("Cycles: " + str(cycles))
    
    if startnode in cycles.keys():
        thiscycle = cycles.pop(startnode)
        for i in range(1, len(thiscycle)):
            val = thiscycle[i]
            key = getkey(val, cycles)

            # conveniently in the keys 
            if val in cycles.keys():
                ecycle += "->" + makeECycle(val, cycles)

            # need to splice another cycle under another startnode
            elif key != None:
                xcycle = cycles[key]
                xindex = xcycle.index(val)
                modcycle = xcycle[xindex:] + xcycle[1:xindex+1]
                cycles.pop(key)
                cycles[val] = modcycle
                ecycle += "->" + makeECycle(val, cycles)

            # no branches
            else:
                ecycle += "->" + val
                    
    else:
        print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")

    return ecycle
    

print(makeECycle(node, cycles))