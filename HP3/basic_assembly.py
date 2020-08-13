from os.path import join
import sys
import time
from collections import defaultdict, Counter
import sys
import os
import zipfile
import argparse
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../.."))

def getkey(val, d):
    for key, v in d.items():
        if val == v:
            return key
    return None

def parse_reads_file(reads_fn):
    """
    :param reads_fn: the file containing all of the reads
    :return: outputs a list of all paired-end reads
    """
    try:
        with open(reads_fn, 'r') as rFile:
            print("Parsing Reads")
            first_line = True
            count = 0
            all_reads = []
            for line in rFile:
                count += 1
                if count % 1000 == 0:
                    print(count, " reads done")
                if first_line:
                    first_line = False
                    continue
                ends = line.strip().split(',')
                all_reads.append(ends)
        return all_reads
    except IOError:
        print("Could not read file: ", reads_fn)
        return None

# from my Stepik 3.10 solution
# generates contigs from a collection of reads with imperfect coverage
def generateContigs():
    contigs = []

    # for each node with outward edges, follow the generated paths while the in/out degrees are valid
    for node in nodeOut.keys():
        if node in nodeIn.keys() and nodeIn[node] == 1 and node in nodeOut.keys() and nodeOut[node] == 1:
            continue
        else:
            for nextNode in paths[node]:
                contig = node
                cur = nextNode

                while cur in nodeIn.keys() and nodeIn[cur] == 1 and cur in nodeOut.keys() and nodeOut[cur] == 1:
                    contig += cur[-1]
                    cur = paths[cur][0]

                contig += cur[-1]
                contigs.append(contig)

    return contigs 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='basic_assembly.py takes in data for homework assignment 3 consisting '
                                                 'of a set of reads and aligns the reads to the reference genome.')
    parser.add_argument('-r', '--reads', required=True, dest='reads_file',
                        help='File containg sequencing reads.')
    parser.add_argument('-o', '--outputFile', required=True, dest='output_file',
                        help='Output file name.')
    parser.add_argument('-t', '--outputHeader', required=True, dest='output_header',
                        help='String that needs to be outputted on the first line of the output file so that the\n'
                             'online submission system recognizes which leaderboard this file should be submitted to.\n'
                             'This HAS to be one of the following:\n'
                             '1) spectrum_A_1_chr_1 for 10K spectrum reads practice data\n'
                             '2) practice_A_2_chr_1 for 10k normal reads practice data\n'
                             '3) hw3all_A_3_chr_1 for project 3 for-credit data\n')
    args = parser.parse_args()
    reads_fn = args.reads_file

    input_reads = parse_reads_file(reads_fn)
    if input_reads is None:
        sys.exit(1)

    # modify reads! treat pairs as independent, split into 25-mers
    all_reads = [item for sublist in input_reads for item in sublist]
    reads_counts = {}
    reads_final = []

    # keep count of 25-mer occurances 
    for read in all_reads:
        for i in range(0, 30):
            kmer = read[i:i+21] 
            if kmer in reads_counts.keys():
                reads_counts[kmer] += 1
            else:
                reads_counts[kmer] = 1

    # remove all 25-mers that occur less than 7 times 
    # this is because they're likely misreads
    for i in range(1, 3): 
        popme = getkey(i, reads_counts)
        while(popme):
            reads_counts.pop(popme)
            popme = getkey(i, reads_counts)

    reads_final = [read for read in reads_counts.keys()]

    # print("\nREADS_COUNTS: " +str(reads_counts))
    # print("\nREADS_FINAL: " +str(reads_final))

    # get paths (nodes with matching prefix/suffix)
    nodelen = len(reads_final[0])-1
    paths = {}
    for gen in reads_final:
        prefix = gen[:nodelen]
        suffix = gen[1:]
        if prefix in paths.keys():
            paths[prefix].append(suffix)
        else:
            paths[prefix] = [suffix]

    # get number of edges in and out of nodes
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

    contigs = generateContigs()
    # print("\nCONTIGS!")
    # for c in contigs:
    #     print(c)

    output_fn = args.output_file
    zip_fn = output_fn + '.zip'
    with open(output_fn, 'w') as output_file:
        output_file.write('>' + args.output_header + '\n')
        output_file.write('>ASSEMBLY\n')
        output_file.write('\n'.join(contigs))
    with zipfile.ZipFile(zip_fn, 'w') as myzip:
        myzip.write(output_fn)
