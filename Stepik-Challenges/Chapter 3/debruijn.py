genome = []
readsfile = open('/Users/katmiao/Desktop/CS122/this.txt', 'r') 
genome = readsfile.read().splitlines()
readsfile.close() 

# reads = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
#         "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"]

def construct(reads):
    for key in reads.keys():
        matches = ""
        for val in reads[key]:
            if matches == "":
                matches = key + " -> " + val
            else: 
                matches += "," + val
        if matches != "":
            print(matches)

genlen = len(genome[0])-1
# genome = ["GAGG","CAGG","GGGG","GGGA","CAGG","AGGG","GGAG"]
reads = {}
for gen in genome:
    prefix = gen[:genlen]
    suffix = gen[1:]
    if prefix in reads.keys():
        reads[prefix].append(suffix)
    else:
        reads[prefix] = [suffix]
#print(reads)

construct(reads)