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

readpairs = []
readsfile = open('/Users/katmiao/Desktop/CS122/3.9/PairedStringReconstruction/inputs/test3.txt', 'r') 
# readsfile = open('/Users/katmiao/Desktop/CS122/3.9/newthis.txt', 'r') #50 200

readpairs = readsfile.read().splitlines()
readsfile.close() 

# get paths (nodes with matching prefix/suffix)
# k = 50
# d = 200
k = 4
d = 2
paths = {}
indexbreak = readpairs[0].index("|")
print("indexbreak: "+str(indexbreak))
for rp in readpairs:
    prefix = (rp[:k-1], rp[indexbreak+1:-1])
    suffix = (rp[1:k], rp[indexbreak+2:])
    if prefix in paths.keys():
        paths[prefix].append(suffix)
    else:
        paths[prefix] = [suffix]
print(paths)
# print("============================================\n"*3)


# get uneven nodes
balanced = {}
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
print("balanced: "+str(balanced))

# find cycles
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
            # print("new cycle: " + startnode +": "+str(cycles[startnode]))
            node = unexplored.pop()
        else:
            # this is the end of the euler path!
            if node in endcycle.keys():
                # print("old: "+str(endcycle))
                # print("adding: "+str(cycle))
                endcycle[startnode] = cycle + endcycle[node][1:]
                endcycle.pop(node)
                # print("new: "+str(endcycle))
                
            else:
                endcycle[startnode] = cycle
            cycle = []
            node = random.choice(list(rempaths))

        startnode = node

if len(rempaths) == 0:
    cycle.append(node)
    cycles[startnode] = cycle

pathstart = getkey(1, balanced)
if (not pathstart):
    rand = balanced.popitem()
    pathstart = rand[0]
    #balanced[rand[0]] = rand[1]

print("\nStart Euler: " + str(pathstart))
print("CYCLES: " + str(cycles))
print("ENDCYCLES: " +str(endcycle))
# print("============================================\n"*3)

# PART 3 - we have the starting node! find path

genome = [None] * 10000

def makeEuler(startindex, startnode, cycles, endcycles):
    if (len(cycles)==0) and (len(endcycles)==0):
        return ""
    
    print("============================================")
    
    # print("This StartNode: " + str(startnode))
    # print("Cycles: " + str(cycles))
    # print("Endcycles: " +str(endcycles))
    # print("StartIndex: "+ str(startindex))

    euler = startnode[0][-1]
    genome[startindex] = euler
    genome[startindex+k+d] = startnode[1][-1]
    # print("GENOME: "+ str(genome))

    

    # check if startnode is a key in cycles
    thiscycle = cycles.pop(startnode, None)
    keyInCycles = getkeylist(startnode, cycles)

    # startnode is in a cycle in cycles, rearrange
    if (thiscycle == None) and (keyInCycles != None):
        spliceCycle = cycles.pop(keyInCycles)
        spliceIndex = spliceCycle.index(startnode)
        modcycle = spliceCycle[spliceIndex:] + spliceCycle[1:spliceIndex+1]
        thiscycle = modcycle
        print("new this (modcycle): "+str(modcycle))
    elif (thiscycle == None) and (startnode in endcycles.keys()):
        thiscycle = endcycles.pop(startnode)
    
    if thiscycle != None:
        print("thiscycle: "+str(thiscycle))
        val = thiscycle[0]

        for i in range(1, len(thiscycle)):
            val = thiscycle[i]
            keyInCycles = getkeylist(val, cycles)
            
            print("i: "+str(i))
            print("val: "+str(val))    

            # conveniently in the keys 
            if val in cycles.keys():
                genome[startindex+i] = val[0][-1]
                genome[startindex+k+d+i] = val[1][-1]
                # print("genome: " + str(genome))
                euler += "->" + makeEuler(startindex+i, val, cycles, endcycle)
                

            # need to splice another cycle under another startnode
            elif keyInCycles != None:
                spliceCycle = cycles.pop(keyInCycles)
                spliceIndex = spliceCycle.index(val)
                modcycle = spliceCycle[spliceIndex:] + spliceCycle[1:spliceIndex+1]
                cycles[val] = modcycle
                print("modcycle: "+str(modcycle))
                euler += "->" + makeEuler(startindex+i, val, cycles, endcycle)

            # no branches in cycles, look at endcycles
            elif val in endcycles.keys():
                print("ayy")
                spliceCycle = endcycles.pop(val)

                if len(spliceCycle) > 1:
                    nextval = spliceCycle[1]
                    endcycles[nextval] = spliceCycle[1:]
                    genome[startindex+i] = val[0][-1]
                    genome[startindex+k+d+i] = val[1][-1]
                    euler += "->" + val[0][-1] + "->" + makeEuler(startindex+i+1, nextval, cycles, endcycles)
                else:
                    euler += "->" + val[0][-1]

            else:
                genome[startindex+i] = val[0][-1]
                genome[startindex+k+d+i] = val[1][-1]
                # print("genome: " + str(genome))
                euler += "->" + val[0][-1]

        if len(thiscycle) == 1:
            return euler
        return euler + makeEuler(startindex, val, cycles, endcycles)[1:]

    # else:
        # print("shit idk")
    
    return euler
    
print(pathstart)
print(pathstart[0][:k-2]+makeEuler(k-2, pathstart, cycles, endcycle))
#print(genome)

genomestr = pathstart[0][:k-2]
for i in genome:
    if i != None:
        genomestr += i

print("FINAL GENOME: " + genomestr)