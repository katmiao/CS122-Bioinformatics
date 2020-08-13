import sys
sys.setrecursionlimit(10**5) 

# ====================================== 
# 5.8 longest path in DAG
# ====================================== 

import re

class Node():
    def __init__(self, num):
        self.children = {}
        self.num = num

def BFS_GRAPH(nodes, start, end):
    start_node = nodes[start]
    return BFS_HELPER(start_node, nodes, start, end)

def BFS_HELPER(cur, nodes, start, end):
    if cur.num == end:
        return (0,end)
    if len(cur.children.keys()) == 0:
        return (0,'x')
    else:
        return_strs = []
        for child in cur.children.keys():
            if child != None:
                val, string = BFS_HELPER(child, nodes, start, end)
                # print(val)
                return_strs.append(( val + int(cur.children[child]) , string ))
                
    ended = list(filter(lambda x : 'x' not in x[1], return_strs))
    if len(ended) == 0:
        return (0, str(cur.num))
        
    ret = max(return_strs, key=lambda x: x[0])
    return (ret[0], str(cur.num) + '->' + str(ret[1]))

def construct_graph(connections):
    nodes = {}
    for begin, end, value in connections:
        begin_node = nodes.get(begin, None)
        if not begin_node:
            nodes[begin] = Node(begin)
            begin_node = nodes[begin]
        
        end_node = nodes.get(end, None)
        if not end_node:
            nodes[end] = Node(end)
            end_node = nodes[end]
        begin_node.children[end_node] = value
    return nodes

def longestPath():
    connections = []
    with open('edges.txt', 'r') as f:
        line = f.readline()
        start = line.rstrip()
        line = f.readline()
        end = line.rstrip()
        
        line = f.readline().rstrip()
        while line:
            obj = re.search(r'(\d+)->(\d+):(\d+)', line)
            connections.append((obj[1],obj[2],obj[3]))
            line = f.readline().rstrip()
            
    # print("connections: " + str(connections))
    nodes = construct_graph(connections)
    ret = BFS_GRAPH(nodes, start, end)
    print(ret[0])
    print(ret[1])

# longestPath()

# ====================================== 
# 5.10 global alignment problem
# ====================================== 
from pprint import pprint
from collections import defaultdict

blosum = {}

with open('BLOSUM62.txt', 'r') as f:
    line = f.readline()
    letline = line.rstrip()
    letters = letline.split()

    line = f.readline().rstrip()
    while line:
        penalties = line.split()
        letter = penalties[0]
        for i in range(1,21):
            blosum[(letter, letters[i-1])] = penalties[i]
        line = f.readline().rstrip()

def makePath(predecessors, s1, s2):
    # print("==== PREDECESSORS ====")
    # print(predecessors)
    backtrack = defaultdict(int)
    path_lengths = defaultdict(lambda:float('-inf'))

    end = (len(s2), len(s1))
    path_lengths[(0,0)] = 0
    for node in predecessors.keys():
        for pred in predecessors[node]:
            if path_lengths[pred] + int(predecessors[node][pred]) > path_lengths[node]:
                path_lengths[node] = path_lengths[pred] + int(predecessors[node][pred])
                backtrack[node] = pred

    node = end
    path = [end]
    while node != 0:
        node = backtrack[node]
        path.append(node)
    print(path)
    return (path_lengths[end], path)

def globalAlignment():
    s1 = "PLEASANTLY"
    s2 = "MEANLY"

    connections = defaultdict(dict)
    for x in range(0, len(s1)+1):
        for y in range(0, len(s2)+1):
            node = (y, x)
            if x < len(s1):
                next = (y, x+1)
                connections[next][node] = -5
            if y < len(s2):
                next = (y+1, x)
                connections[next][node] = -5
            if x < len(s1) and y < len(s2):
                next = (y+1, x+1)
                score = int(blosum[(s1[x], s2[y])])
                connections[next][node] = score
    # print(connections)
    score, steps = makePath(connections, s1, s2)
                
    # nodes = construct_graph(connections)
    # ret = BFS_GRAPH(nodes, (0,0), (len(s2), len(s1)))

    # score = ret[0]
    # path = ret[1]
    # print(path)

    # steps = path.split("->")
    steps.pop()
    prev = steps.pop() #0
    # obj = re.search(r'\((\d+), (\d+)\)', prev)
    print(prev)
    # prev = (int(obj[1]), int(obj[2]))
    a1 = ""
    a2 = ""
    # for step in steps:
    for step in reversed(steps):
        print("step: " + str(step))
        # obj = re.search(r'\((\d+), (\d+)\)', step)
        # x = int(obj[1])
        # y = int(obj[2])
        x, y = step
        # print("x="+str(x) + ", y=" + str(y) + ", prev=" + str(prev))
        if x == prev[0]:
            a2 += "-"
            a1 += s1[prev[1]]
        elif y == prev[1]:
            a1 += "-"
            a2 += s2[prev[0]]
        else:
            a1 += s1[prev[1]]
            a2 += s2[prev[0]]
        # print(a1)
        # print(a2)
        prev = (x, y)

    print(score)
    print(a1)
    print(a2)

# globalAlignment()

# ====================================== 
# 5.10 local alignment problem
# ====================================== 

def makeLocalPath(predecessors, s1, s2):
    # print("==== PREDECESSORS ====")
    # print(predecessors)
    backtrack = defaultdict(int)
    path_lengths = defaultdict(lambda:float('-inf'))

    end = (len(s2), len(s1))
    path_lengths[(0,0)] = 0
    path_lengths[(len(s2), len(s1))] = 0
    for node in predecessors.keys():
        for pred in predecessors[node]:
            print("predecessor: " + str(node) + ", " + str(pred))
            print("---> " + str(path_lengths[pred]) + ", " + str(predecessors[node][pred]) + ", " + str(path_lengths[node]))

            if path_lengths[pred] + int(predecessors[node][pred]) > path_lengths[node]:
                
                path_lengths[node] = path_lengths[pred] + int(predecessors[node][pred])
                backtrack[node] = pred
                print("---> " + str(path_lengths[node]) + ", " + str(backtrack[node]))


    node = end
    path = [end]
    while node != 0:
        node = backtrack[node]
        path.append(node)
    # print(path_lengths[end])
    # print(path)
    return (path_lengths[end], path)

def localAlignment():
    s1 = "MEANLY"
    s2 = "PENALTY"

    # s1 = "AMTAFRYRQGNPRYVKHFAYEIRLSHIWLLTQMPWEFVMGIKMPEDVFQHWRVYSVCTAEPMRSDETYEQKPKPMAKWSGMTIMYQAGIIRQPPRGDRGVSDRNYSQCGKQNQAQLDNNPTWTKYEIEWRVQILPPGAGVFEGDNGQNQCLCPNWAWEQPCQWGALHSNEQYPNRIHLWAPMSKLHIKIEKSSYNRNAQFPNRCMYECEFPSYREQVDSCHYENVQIAFTIFSGAEQKRKFCSCHFWSNFIDQAVFSTGLIPWCYRRDDHSAFFMPNWNKQYKHPQLQFRVAGEGTQCRPFYTREMFTKVSAWRIAGRFAGPYERHHDAHLELWYQHHKVRTGQQLGIIWNNRDKTRNPCPFSAYYNKLPWWKINQNAFYNCLQNIAHSTHDETHEFNPVKCIDWLQGTMVPTECKKGFVHEKCECYRNPGPPLHDMYHQMEDIFGVRFDCLTGWKHLSDYNPCQERRNINDFYIFAYEIAPAVKNLVLSPQPLADATKKCAFNYTPLDQSPVVIACKWYIHQPICMLLIVLICAMDKYNAHMIVIRTTEGQQPMHACRMTEGPGMCMKEPLVTFTLPAQWQWPNHEFKYVYMYVLNYHLSQYTYTDEGHAGGQHYSFNVAVDVGMAWGHNRCYCQPACYSQQETQTRTIDYEKWQYMKHQAFKWGLWFCEQERHAWFKGQNRCEMFTAKMTRMGADSNLDQYKLMLAQNYEEQWEQPIMECGMSEIIEIDPPYRSELIFTFWPFCTYSPWQNLIKCRCNNVIEEMDQCVPLTFIGFGVKQAGGIQAWAFYKEEWTSTYYLMCQCMKSDKAQYPYEIILFWMQPMDTGEQEPPQQNMWIFLPHSWFFDWCCNAPWSEICSSRHDHGQCQDAFYPCELFTVFDDIFTAEPVVCSCFYDDPM"
    # s2 = "WQEKAVDGTVPSRHQYREKEDRQGNEIGKEFRRGPQVCEYSCNSHSCGWMPIFCIVCMSYVAFYCGLEYPMSRKTAKSQFIEWCDWFCFNHWTNWAPLSIVRTSVAFAVWGHCWYPCGGVCKTNRCKDDFCGRWRKALFAEGPRDWKCCKNDLQNWNPQYSQGTRNTKRMVATTNQTMIEWKQSHIFETWLFCHVIIEYNWSAFWMWMNRNEAFNSIIKSGYPKLLLTQYPLSQGSTPIVKPLIRRDQGKFWAWAQMWWFREPTNIPTADYCHSWWQSRADLQNDRDMGPEADASFYVEFWYWVRCAARTYGQQLGIIWNNRLKTRNPCPYSADGIQNKENYVFWWKNMCTKSHIAFYYCLQNVAHYTHDVTAEFNPVKCIDWLQGHMVLSSWFKYNTECKKLFVHEKCECYRMFCGVVEDIFGVRFHTGWKHLSTAKPVPHVCVYNPSVQERRNINDFYIFYEIAPAVKNLVLSAQPLHDYTKKCAFNYTPITITRIISTRNQIIWAHVVIACQFYSPHQMLLIELAMDKYCADMNVRRSTEGHQPMHACRSTFGPGMAAKEPLVTFTLVAFWQWPNHEFQYVYMYTEDKIIQIGPHLSNGCEMVEYCVDCYAKRPCYRAYSAEAQYWRMITEAEDYSYKTRNAIAATATVRGQYCHPFRWLGIVWMAHHDCFFANECGTICIPQMAEMRPPETTPYEIDIIFMMFWKEHMSTTILDVVGMYRPATFSHWHDAHHQCEPYLTPLMCQSKLVFDAAFTQVGVKGVWYHTEKLELMAGFNHMKFKKEEAQQSCFYWFQDCPDYDPPDAVRKTDEKHIRAHGEIWWLMRYYCMYHILHIASRHEWMHLRWDQACTNPGYELFEFIPWVLRRYVVYDKIRYNYSYRNSASMEFV"

    connections = defaultdict(dict)
    for x in range(0, len(s1)+1):
        for y in range(0, len(s2)+1):
            print("x="+str(x) + ", y=" + str(y))
            # print("s1[x]=" + s1[x] + ", s2[y]=" + s2[y])

            node = (y, x)

            if x == 0 and y == 0:
                connections[(y, x+1)][node] = 0
                connections[(y+1, x)][node] = 0
                connections[(y+1, x+1)][node] = int(blosum[(s1[x], s2[y])])
                continue

            elif x == len(s1) and y == len(s2):
                continue

            elif x > 1 or y > 1:
                connections[node][(0,0)] = 0
                print("A")
                if not (x == len(s1) and y == len(s2)):
                    connections[(len(s2), len(s1))][node] = 0
                    print("B")

            if x < len(s1):
                next = (y, x+1)
                connections[next][node] = -5
                print("C")
            if y < len(s2):
                next = (y+1, x)
                connections[next][node] = -5
                print("D")
            if x < len(s1) and y < len(s2):
                next = (y+1, x+1)
                score = int(blosum[(s1[x], s2[y])])
                print("E " + str(score))
                connections[next][node] = score

            # if (x-1 == 0 and y-1 == 0) or (x-1 == 0 and y == 0) or (x == 0 and y-1 == 0): 
            #     print("F")
                # connections[node][(0,0)] = max(0, int(blosum[(s1[x-1], s2[y-1])]))
            if (x+1 == len(s1) and y+1 == len(s2)) :
                print("G" + (blosum[(s1[x], s2[y])]))
                connections[(len(s2), len(s1))][node] = max(0, int(blosum[(s1[x], s2[y])]))
            elif (x+1 == len(s1) and y == len(s2)) or (x == len(s1) and y+1 == len(s2)):
                print("H")
                connections[(len(s2), len(s1))][node] = 0


            # print("==== CONNECTIONS ====")
            pprint(connections)
    print("==== CONNECTIONS ====")
    pprint(connections)
    score, steps = makeLocalPath(connections, s1, s2)
                
    steps.pop()
    prev = steps.pop() 
    a1 = ""
    a2 = ""
    for step in reversed(steps):
        x, y = step
        # print("x="+str(x) + ", y=" + str(y) + ", prev=" + str(prev))
        if not (((x - prev[0] == 1) and (y == prev[1])) or ((x == prev[0]) and (y - prev[1] == 1)) or ((x - prev[0] == 1) and (y - prev[1] == 1))):
            prev = (x, y)
            continue
        if x == prev[0]:
            a2 += "-"
            a1 += s1[prev[1]]
        elif y == prev[1]:
            a1 += "-"
            a2 += s2[prev[0]]
        else:
            a1 += s1[prev[1]]
            a2 += s2[prev[0]]
        # print(a1)
        # print(a2)
        prev = (x, y)

    print(score)
    print(a1)
    print(a2)

localAlignment()