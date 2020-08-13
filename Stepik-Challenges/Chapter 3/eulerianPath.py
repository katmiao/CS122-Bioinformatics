import random

def getkey(val, d):
    for key, v in d.items():
        if val == v:
            return key
    return None

def getkeylist(val, d):
    for key, vals in d.items():
        if val in vals:
            return key
    return None

# PART 1 - parse file
paths = {}
readsfile = open('/Users/katmiao/Desktop/CS122/db.txt', 'r') 
balanced = {}
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

# get uneven nodes
for node in paths.keys():
    edges = paths[node]
    if node in balanced.keys():
        balanced[node] += len(edges)
    else:
        balanced[node] = len(edges)
    for edge in edges:
        if edge in balanced.keys():
            balanced[edge] -= 1
        else:
            balanced[edge] = -1

# PART 2 - find the startnode and find cycles
rempaths = paths.copy()
cycles = {}         # key: startnode, val: cycle in list
endcycle = {}
node = random.choice(list(rempaths))
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

        if (len(unexplored) > 0) and (startnode == node):
            # log cycle
            cycles[startnode] = cycle
            cycle = []
            node = unexplored.pop()
        else:
            # this is the end of the euler path!
            if node in endcycle.keys():
                endcycle[startnode] = cycle + endcycle[node][1:]
                endcycle.pop(node)                
            else:
                endcycle[startnode] = cycle
            cycle = []
            node = random.choice(list(rempaths))

        startnode = node

if len(rempaths) == 0:
    cycle.append(node)
    cycles[startnode] = cycle

pathstart = getkey(1, balanced)
print("Start Euler: " + pathstart)
print("CYCLES: " + str(cycles))
print("ENDCYCLES: " +str(endcycle))

# PART 3 - we have the starting node! find path

def makeEuler(startnode, cycles, endcycles):
    euler = str(startnode)
    # print("This StartNode: " + startnode)
    # print("Cycles: " + str(cycles))
    # print("Endcycles: " +str(endcycles))

    # check if startnode is a key in cycles
    thiscycle = cycles.pop(startnode, None)
    keyInCycles = getkeylist(startnode, cycles)

    # startnode is in a cycle in cycles, rearrange
    if (thiscycle == None) and (keyInCycles != None):
        spliceCycle = cycles.pop(keyInCycles)
        spliceIndex = spliceCycle.index(startnode)
        modcycle = spliceCycle[spliceIndex:] + spliceCycle[1:spliceIndex+1]
        thiscycle = modcycle
        # print("new this (modcycle): "+str(modcycle))
    elif (thiscycle == None) and (startnode in endcycles.keys()):
        thiscycle = endcycles.pop(startnode)
    
    if thiscycle != None:
        # print("thiscycle: "+str(thiscycle))
        val = thiscycle[0]
        for i in range(1, len(thiscycle)):
            val = thiscycle[i]
            keyInCycles = getkeylist(val, cycles)
            
            # print("val: "+val)            

            # conveniently in the keys 
            if val in cycles.keys():
                euler += "->" + makeEuler(val, cycles, endcycle)

            # need to splice another cycle under another startnode
            elif keyInCycles != None:
                spliceCycle = cycles.pop(keyInCycles)
                spliceIndex = spliceCycle.index(val)
                modcycle = spliceCycle[spliceIndex:] + spliceCycle[1:spliceIndex+1]
                cycles[val] = modcycle
                # print("modcycle: "+str(modcycle))
                euler += "->" + makeEuler(val, cycles, endcycle)

            # no branches in cycles, look at endcycles
            elif val in endcycles.keys():
                # print("ayy")
                spliceCycle = endcycles.pop(val)

                if len(spliceCycle) > 1:
                    nextval = spliceCycle[1]
                    endcycles[nextval] = spliceCycle[1:]
                    euler += "->" + val + "->" + makeEuler(nextval, cycles, endcycles)
                else:
                    euler += "->" + val

            else:
                euler += "->" + val

        if len(thiscycle) == 1:
            return euler
        return euler + makeEuler(val, cycles, endcycles)[len(val):]

    # else:
        # print("shit idk")
    
    return euler
    

print(makeEuler(pathstart, cycles, endcycle))