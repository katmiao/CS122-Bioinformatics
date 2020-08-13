import sys
sys.setrecursionlimit(10**5) 

# ====================================== 
# 5.6 manhattan tourist problem
# ====================================== 

def MTourist(n, m, Down, Right):
    s = [[0] * (m+1) for i in range(n+1)]
    for i in range(1, n + 1):
        s[i][0] = s[i-1][0] + Down[i-1][0]
    for j in range(1, m + 1):
        s[0][j] = s[0][j-1] + Right[0][j-1]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s[i][j] = max(s[i-1][j] + Down[i-1][j], s[i][j-1] + Right[i][j-1])

    return s[n][m]

def CallMTourist():
    down = []
    right = []
    downfile = open('/Users/katmiao/Desktop/CS122/5/down.txt', 'r') 
    downrows = downfile.read().splitlines()
    downfile.close() 
    for row in downrows:
        row = row.split(' ')
        row = [int(i) for i in row]
        down.append(row)

    rightfile = open('/Users/katmiao/Desktop/CS122/5/right.txt', 'r') 
    rightrows = rightfile.read().splitlines()
    rightfile.close() 
    for row in rightrows:
        row = row.split(' ')
        row = [int(i) for i in row]
        right.append(row)

    n = 18
    m = 10
    print(MTourist(n, m, down, right))
# CallMTourist()

# ====================================== 
# 5.6 manhattan tourist problem
# ====================================== 

def LCSBacktrack(v, w):
    s = [ [0 for i in range(len(w)+1)] for j in range(len(v)+1) ]

    for i in range(0, len(v)+1):
        s[i][0] = 0
    for j in range(0, len(w)+1):
        s[0][j] = 0

    backtrack = {}
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):
            match = 0
            if v[i-1] == w[j-1]:
                match = 1
            s[i][j] = max(s[i-1][j], s[i][j-1], s[i-1][j-1] + match)
            if s[i][j] == s[i-1][j]:
                backtrack[(i,j)] = "down"
            elif s[i][j] == s[i][j-1]:
                backtrack[(i,j)] = "right"
            elif s[i][j] == s[i-1][j-1] + match:
                backtrack[(i,j)] = "diag"
    print("BACKTRACK: " + str(backtrack))
    return backtrack
        

def OutputLCS(backtrack, v, i, j):
    print("i="+str(i)+". j="+str(j))
    if i == 0 or j == 0:
        return ""
    if backtrack[(i,j)] == "down":
        return OutputLCS(backtrack, v, i - 1, j)
    elif backtrack[(i,j)] == "right":
        return OutputLCS(backtrack, v, i, j - 1)
    elif backtrack[(i,j)] == "diag":
        return OutputLCS(backtrack, v, i - 1, j - 1) + v[i-1]
    else:
        print("wtf")
        return ""

def CallLCS():
    v = "GCCGGAACCTAGTCATCTCTGTCGAACTGGTGGACTATCCAAAACTAGCACTTAAGTGCACATTATCGCCTACTATGCCGCGATAAGAGCCATCTACGTGGCAGCAGACGTGGGCCCGCTGGCTATTACTCCTAGACCGACTGTGAGCATTAGGCGTGCTAGCTCTCAGTACGAATAGCTCGAGCGTCTTTCGGTGCAGCTATTAGTCGTTACAACACCCAATATTTCACTGAATCACAGTATGCGTGGTACGTGCGTGCTACATTCCTCATTCGGAACAGGATATTAAAGCGGGGTTGGGACATGTAATTTGATACGAAGAGTCAAGGGTCTGGTACTAACCCTCAACAAGTACTATGTCAGCGAAGTTAATGTGTATACGCGGCGTAAGAGTTGCTTACTCGTTCTGCGCGGTGGCAAACCACTGGCTGTGGCTCCCGCCATTTTGACCCCCCAACTTGACAACTGTCGAATGAGCCGTGTCCTTCACGCTAGTTGGACGGTCCATTCGGCATTGTGGCAACTGGGATAAGCTTAACGTAATCGTGCCTGTACACCCCACACGGCGCCGAACTGGAAAATAGGGTAACGCAATGGGGAATTCTCTCCTGAACGTTGCGTTAGCGCTCTAACAGGCGCGGCTTTTATCCACTACCCTCTATGGACGCGCGTGCGAAAATTCAGAACGCCTGGAAGAGAGTTGATGCACTCCTACTAGGTCTAACTTATATACATGAGCGCTTCACTGGCAGGGTGCCAACTAGGCGCCCCGTTTGGTCTCGGATCCCGACCCTGTCTAATGATGCGTGTTGTGTCAACACCAATAGCATGCGACGCAATACGGCCAAACCGTGCGGTGTGTTATGGACCCTTGGTGAATTCCTTCCGATATGGAACTATACCGGAGTCGCCCTAGCTATGCCGATATCCAAGTCGCTGAGAGTGAATTACCGGTAGTTGAGGTGATGA"
    w = "CTCTAAGCGTGCAGCGACTTTCTCGTCAGAAATAGCGGCCTTCGATTTATTACATCTTCACGCCTTGTCTGGGTGGCGTTAATCGTTTTCGAGTAATTTCCATTACTAAACCCGACCTATTGAGGTCGTACTGGAGTAGAAGCAGCGTCTCGACCCTTAATCTATGGCCCCCCGGTCCTGTGTGCTCCATAGATTCTCCCGCTTTAGGACGGCATCTAGCTATTATGTCGCATACAACTATCACTGAATAGCGGATTCTCGAAACAGCGGTGATTCATACCCTCGCCGTCGACGGCGTACTACAACATGCTGCATTCGTTATGTTTTAAGCGATACGAGAGTTACCCCGTCAGATCCCCGATAGGGGCTCCGCTTATTTTAAAAGCGGCCCGGCCTTGCGCGGATTCTTGCTCAACTGTGTCTAGCCACTATCCCGCGCCGAATCTAATGTTCGTGCGTCGTTGTTAGGAGGTCCTGAGGGCGTTCCCCCCCTATCCTAATTGCTCATCGTCCAGTGTGATTCCTCCCGACTAACGGCATAAATATGTGTGGACGTTTCCCACACATACTGTCAATCCCAATAAGGAAGTGCTTCGGGGTTCTTGTTGGCCCCGCGCAGTGCACGATTCATCCCAGTTGGAAATGGAGGAATCTAATATCCCCATTCCGTAACTAATTTGTTCTTTCGTCCGAACACGATGTAGGCGTAGCCAAAACATTTGCCTCGGGTACCATGGTTGGTAAGGAACTACGTTTCTGCGCATTTTCTTAACCGGTATCAGACTCCCCTCATACTACCTCATTGCTATTTTCAAGGATCTTCATCTTACTTGTCACTAAGGTTGCTGTTGGACCTGTCAGGTAAACGTC"
    backtrack = LCSBacktrack(v, w)
    print(OutputLCS(backtrack, v, len(v), len(w)))

# CallLCS()

