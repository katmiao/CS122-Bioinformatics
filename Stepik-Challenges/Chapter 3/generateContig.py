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

reads = []
readsfile = open('/Users/katmiao/Desktop/CS122/3.10/final.txt', 'r') 

reads = readsfile.read().splitlines()
readsfile.close() 

# get paths (nodes with matching prefix/suffix)
nodelen = len(reads[0])-1
paths = {}
for gen in reads:
    prefix = gen[:nodelen]
    suffix = gen[1:]
    if prefix in paths.keys():
        paths[prefix].append(suffix)
    else:
        paths[prefix] = [suffix]

# print(paths)

# get uneven nodes
nodeIn = {}
nodeOut = {}
for node in paths.keys():
    edges = paths[node]
    if node in nodeOut.keys():
        nodeOut[node] += len(edges)
    else:
        nodeOut[node] = len(edges)
    for edge in edges:
        if edge in nodeIn.keys():
            nodeIn[edge] += 1
        else:
            nodeIn[edge] = 1

# print("nodeIn: "+str(nodeIn))
# print("nodeOut: "+str(nodeOut))
# print("============================================")

def generateContigs():
    contigs = []
    for node in nodeOut.keys():
        if node in nodeIn.keys() and nodeIn[node] == 1 and node in nodeOut.keys() and nodeOut[node] == 1:
            continue
        else:
            for nextNode in paths[node]:
                contig = node
                cur = nextNode
                # print("contig: "+contig)
                # print("cur: "+cur)
                while cur in nodeIn.keys() and nodeIn[cur] == 1 and cur in nodeOut.keys() and nodeOut[cur] == 1:
                    contig += cur[-1]
                    cur = paths[cur][0]
                    # print("new contig: "+contig)
                    # print("new cur: "+cur)

                contig += cur[-1]
                
                # if contig not in contigs:
                contigs.append(contig)

    return contigs  
    
contigs = generateContigs()
print(" ".join(contigs))

