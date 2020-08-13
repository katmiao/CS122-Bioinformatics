import sys
import argparse
import time
import zipfile
from collections import defaultdict


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


def parse_ref_file(ref_fn):
    """
    :param ref_fn: the file containing the reference genome
    :return: a string containing the reference genome
    """
    try:
        with open(ref_fn, 'r') as gFile:
            print("Parsing Ref")
            first_line = True
            ref_genome = ''
            for line in gFile:
                if first_line:
                    first_line = False
                    continue
                ref_genome += line.strip()
        return ref_genome
    except IOError:
        print("Could not read file: ", ref_fn)
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='basic_aligner.py takes in data for homework assignment 1 consisting '
                                     'of a genome and a set of reads and aligns the reads to the reference genome, '
                                     'then calls SNPs based on this alignment')
    parser.add_argument('-g', '--referenceGenome', required=True, dest='reference_file',
                        help='File containing a reference genome.')
    parser.add_argument('-r', '--reads', required=True, dest='reads_file',
                        help='File containg sequencing reads.')
    parser.add_argument('-o', '--outputFile', required=True, dest='output_file',
                        help='Output file name.')
    parser.add_argument('-t', '--outputHeader', required=True, dest='output_header',
                        help='String that needs to be outputted on the first line of the output file so that the '
                             'online submission system recognizes which leaderboard this file should be submitted to.'
                             'This HAS to be practice_W_1_chr_1 for the practice data and hw1_W_2_chr_1 for the '
                             'for-credit assignment!')
    args = parser.parse_args()
    reference_fn = args.reference_file
    reads_fn = args.reads_file

    input_reads = parse_reads_file(reads_fn)
    if input_reads is None:
        sys.exit(1)
    reference = parse_ref_file(reference_fn)
    if reference is None:
        sys.exit(1)

    # modify reads! treat pairs as independent
    all_reads = [item for sublist in input_reads for item in sublist]
    reads_counts = {}
    reads_final = []

    # get 25-mers 
    for read in all_reads:
        firstHalf = read[:25]
        lastHalf = read[25:]
        for kmer in [firstHalf, lastHalf]:
            reads_final.append(kmer)

    # print("\nREADS_COUNTS: " +str(reads_counts))
    # print("\nREADS_FINAL: " +str(reads_final))

    # make dictionary out of reference genome
    refDict = {}
    indexRef = defaultdict(list)
    for i in range(0, len(reference)-25):
        kmer = reference[i:i+25]
        indexRef[kmer].append(i)
    
    # find all mutations
    for read in reads_final:
        if read in indexRef.keys():
            # perfect match! u gucci
            # print("perfect match: " + read)
            continue
        else:
            for kmer in indexRef.keys():
                for i in range(0, len(kmer)-1):
                    if (read[:i] == kmer[:i]) and (read[i+1:] == kmer[i+1:]):
                        # print("mutation: read=" + read[i] + " ref=" + kmer[i] + " i=" + str(i))
                        if kmer in refDict:
                            refDict[kmer].append((read[i], kmer[i], i))
                        else:
                            refDict[kmer] = [(read[i], kmer[i], i)]
                        continue
    print("\nREFDICT: " + str(refDict))

    # refDict = savedRefDict # from testing

    # once keeps track of all muts that have appeared once. a mut is only added to indexToMuts after it has appeared twice, to mitigate read errors 
    once = []
    mutations = []
    indexToMuts = {}
    print("\nREFDICT: " + str(refDict))

    # map all indexes to their mutatinos
    for kmer, differences in refDict.items():
        for diff in differences:
            if diff in once:
                for i in indexRef[kmer]:
                    genomeIndex = diff[2] + i
                    mut = [diff[1], diff[0], genomeIndex]

                    if genomeIndex in indexToMuts.keys():
                        indexToMuts[genomeIndex].append((diff[1], diff[0]))
                    else: 
                        indexToMuts[genomeIndex] = [(diff[1], diff[0])]
            else:
                once.append(diff)

    
    print("\nindexToMuts: " + str(indexToMuts))

    
    for index, muts in indexToMuts.items():
        # mutation only appears twice (we filtered out single appearances above), likely a misread
        if len(muts) == 1:
            continue
        else:
            # there's several mutations, make sure they're consistent!
            print("index: "+ str(index) + " muts: " + str(muts))

            consistent = True
            inconsistent = 0
            for mut in muts:
                if mut != muts[0]:
                    consistent = False
                    inconsistent += 1

            # if there's an inconsistency, find the most common mutation if it exists
            if consistent == False:
                if len(muts) - inconsistent <= 1:
                    # tie, can't identify which is a misread so don't include
                    print("   inconsistent! not adding")
                    continue
                else:
                    for i in range(0, len(muts)-1):
                        if muts[i] == muts[i+1]:
                            snp = [muts[i][0], muts[i][1], index]
                            print("   winner: "+str(snp))
                            mutations.append(snp)
                            break

            # consistent, it's a snp!
            if consistent:
                snp = [muts[0][0], muts[0][1], index]
                mutations.append(snp)

    print("\nMutations: " + str(mutations))

    snps = mutations

    output_fn = args.output_file
    zip_fn = output_fn + '.zip'
    with open(output_fn, 'w') as output_file:
        header = '>' + args.output_header + '\n>SNP\n'
        output_file.write(header)
        for x in snps:
            line = ','.join([str(u) for u in x]) + '\n'
            output_file.write(line)

        tails = ('>' + x for x in ('STR', 'CNV', 'ALU', 'INV', 'INS', 'DEL'))
        output_file.write('\n'.join(tails))

    with zipfile.ZipFile(zip_fn, 'w') as myzip:
        myzip.write(output_fn)
