# Katherine Miao 
# scores SNPs 75.51, indels 53.1

import sys
import argparse
import numpy as np
import time
import zipfile
from collections import defaultdict


def parse_reads_file(reads_fn):
    """
    :param reads_fn: the file containing all of the reads
    :return: outputs a list of all paired-end reads

    HINT: This might not work well if the number of reads is too large to handle in memory
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


"""
    TODO: Use this space to implement any additional functions you might need

"""
def HammingDistance(s1, s2):
    if len(s1) != len(s2): return float('inf')
    return sum(1 if s1[i] != s2[i] else 0 for i in range(len(s1)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='basic_hasher.py takes in data for homework assignment 2 consisting '
                                     'of a genome and a set of reads and aligns the reads to the reference genome, '
                                     'then calls SNPS and indels based on this alignment.')
    parser.add_argument('-g', '--referenceGenome', required=True, dest='reference_file',
                        help='File containing a reference genome.')
    parser.add_argument('-r', '--reads', required=True, dest='reads_file',
                        help='File containg sequencing reads.')
    parser.add_argument('-o', '--outputFile', required=True, dest='output_file',
                        help='Output file name.')
    parser.add_argument('-t', '--outputHeader', required=True, dest='output_header',
                        help='String that needs to be outputted on the first line of the output file so that the\n'
                             'online submission system recognizes which leaderboard this file should be submitted to.\n'
                             'This HAS to be one of the following:\n'
                             '1) practice_W_3_chr_1 for 10K length genome practice data\n'
                             '2) practice_E_1_chr_1 for 1 million length genome practice data\n'
                             '3) hw2undergrad_E_2_chr_1 for project 2 undergrad for-credit data\n'
                             '4) hw2grad_M_1_chr_1 for project 2 grad for-credit data\n')
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
    triple_reads = []

    # get 16-mers 
    for read in all_reads:
        first = read[:16]
        second = read[16:32]
        third = read[32:48]
        triple_reads.append([first, second, third])

    # make dictionary out of reference genome
    refDict = {}
    indexRef = defaultdict(list)
    for i in range(0, len(reference)-16):
        kmer = reference[i:i+16]
        indexRef[kmer].append(i)

    indels = []
    # find all mutations and indels!
    for triple in triple_reads:
        partlyMatches = False
        # will map indexes where each section of the triple matches
        tripleToIndexs = {1:[], 2:[], 3:[]}
        numMismatches = 0

        for tripleIndex in [1, 2, 3]:
            read = triple[tripleIndex-1]
            if indexRef.get(read) != None:
                # perfect match! u gucci
                partlyMatches = True
                tripleToIndexs[tripleIndex].extend(indexRef[read])
                continue
            else:
                numMismatches += 1

        # only deal with triple with 1 mismatching third
        if numMismatches != 1:
            continue

        # base index to inspect for mismatching third based on thirds that matched
        read = ""
        possibleIndexs = []
        refIndex = 100
        offset = 0
        if len(tripleToIndexs[1]) == 0:
            read = triple[0]
            offset = -16
            refIndex = 2
        elif len(tripleToIndexs[2]) == 0:
            read = triple[1]
            offset = 16
            refIndex = 1
        elif len(tripleToIndexs[3]) == 0:
            read = triple[2]
            offset = 16
            refIndex = 2
            
        for i in tripleToIndexs[refIndex]:
            possibleIndexs.append(i + offset)

        # use hamming distance! snps will have hamming distance of 1
        minHamDis = float('inf')
        minHamRef = ""
        for possibleIndex in possibleIndexs:
            ham = HammingDistance(read, reference[possibleIndex:possibleIndex+16])
            if ham < minHamDis:
                minHamDis = ham
                minHamRef = reference[possibleIndex:possibleIndex+16]

        if minHamRef != "" and minHamDis == 1:
            ref = minHamRef
            #  find exact location of snp
            for i in range(0, len(ref)-1):
                if (read[:i] == ref[:i]) and (read[i+1:] == ref[i+1:]):
                    if refDict.get(ref) != None:
                        refDict[ref].append((read[i], ref[i], i))
                    else:
                        refDict[ref] = [(read[i], ref[i], i)]
                    break

        else:       
            # if no SNP mutation was found, this is an indel!
            indels.append(triple)

    ############################## SNP MUTATIONS ##############################

    # once keeps track of all muts that have appeared once. a mut is only added to indexToMuts after it has appeared twice, to mitigate read errors 
    once = []
    mutations = []
    indexToMuts = {}
    
    # map all indexes to their mutatinos
    for kmer, differences in refDict.items():
        for diff in differences:
            if diff in once:
                for i in indexRef[kmer]:
                    genomeIndex = diff[2] + i
                    mut = [diff[1], diff[0], genomeIndex]

                    if indexToMuts.get(genomeIndex) != None:
                        indexToMuts[genomeIndex].append((diff[1], diff[0]))
                    else: 
                        indexToMuts[genomeIndex] = [(diff[1], diff[0])]
            else:
                once.append(diff)
    
    for index, muts in indexToMuts.items():
        # filter out less common mutations, likely misread (filtered out single appearances above)
        if len(muts) <= 2:              # note: this seems to be the max 
            continue
        else:
            print("index: "+ str(index) + " muts: " + str(muts))

            # there's several mutations, make sure they're consistent!
            consistent = True
            inconsistent = 0
            for mut in muts:
                if mut != muts[0]:
                    consistent = False
                    inconsistent += 1
                    break

            # consistent, it's definitely a snp!
            if consistent:
                print("   consistent!")
                snp = [muts[0][0], muts[0][1], index]
                mutations.append(snp)

            # if there's an inconsistency, find the most common mutation if it exists
            if consistent == False:
                
                snpsToCounts = {}
                maxCount = -1
                maxSNPs = ()
                for i in range(0, len(muts)):
                    snp = (muts[i][0], muts[i][1], index)
                    if snpsToCounts.get(snp) != None:
                        snpsToCounts[snp] += 1
                        if snpsToCounts[snp] > maxCount:
                            maxCount = snpsToCounts[snp]
                            maxSNPs = snp
                    else:
                        snpsToCounts[snp] = 1

                ratio = float(maxCount)/float(len(muts))
                print("     maxCount: "+str(maxCount))
                print("     ratio: "+str(ratio))

                # make sure it's the majority by over 2/3rds
                if ratio > 0.67:
                    snp = list(maxSNPs)
                    print("   winner: "+str(snp))
                    mutations.append(snp)
                    continue
                else:
                    print("   inconsistent. not adding")    

    snps = mutations

    ############################## NEW REFERENCE USING SNPS ##############################
    ###### can uncomment this but doesn't improve indel score much, it's rare case #######

    # for snp in snps:
    #     orig, mut, index = snp
    #     reference = reference[:index] + mut + reference[index+1:]

    # # make dictionary out of reference genome
    # refDict = {}
    # indexRef = defaultdict(list)
    # for i in range(0, len(reference)-16):
    #     kmer = reference[i:i+16]
    #     indexRef[kmer].append(i)

    # indels = []
    # # find all mutations and indels
    # for triple in triple_reads:
    #     partlyMatches = False
    #     tripleToIndexs = {1:[], 2:[], 3:[]}
    #     numMismatches = 0

    #     for tripleIndex in [1, 2, 3]:
    #         read = triple[tripleIndex-1]
    #         if indexRef.get(read) != None:
    #             # perfect match! u gucci
    #             partlyMatches = True
    #             tripleToIndexs[tripleIndex].extend(indexRef[read])
    #             continue
    #         else:
    #             numMismatches += 1

    #     if numMismatches != 1:
    #         continue

    #     read = ""
    #     possibleIndexs = []
    #     refIndex = 100
    #     offset = 0
    #     if len(tripleToIndexs[1]) == 0:
    #         read = triple[0]
    #         offset = -16
    #         refIndex = 2
    #     elif len(tripleToIndexs[2]) == 0:
    #         read = triple[1]
    #         offset = 16
    #         refIndex = 1
    #     elif len(tripleToIndexs[3]) == 0:
    #         read = triple[2]
    #         offset = 16
    #         refIndex = 2
            
    #     for i in tripleToIndexs[refIndex]:
    #         possibleIndexs.append(i + offset)

    #     minHamDis = float('inf')
    #     minHamRef = ""
    #     for possibleIndex in possibleIndexs:
    #         ham = HammingDistance(read, reference[possibleIndex:possibleIndex+16])
    #         if ham < minHamDis:
    #             minHamDis = ham
    #             minHamRef = reference[possibleIndex:possibleIndex+16]
    #     if minHamRef != "" and minHamDis == 1:
    #         continue
    #     else:       
    #         # if no SNP mutation was found, this is an indel!
    #         indels.append(triple)

    ############################## INDELS ##############################
    insertions = []
    deletions = []
    # to make sure indels aren't from read errors
    onceInsertions = []
    onceDeletions = []

    for indel in indels:
        first, second, third = indel
        read = first + second + third
        startIndexs = indexRef[first]
        
        for index in startIndexs:
            i = 0
            # find index where read diverges from reference
            while read[i] == reference[index + i]:
                i += 1
            
            maxIndelLen = 5
            for indelLen in range(1, maxIndelLen+1):
                # check for insertion
                if read[i+indelLen:i+5+indelLen] == reference[index+i:index+i+5]:
                    insertTup = (read[i:i+indelLen], index+i)
                    if insertTup in onceInsertions:
                        # print("full read: " + read + " --- indel at: " + str(i))
                        # print("     read: " + read[i:i+20])
                        # print("     ref : " + reference[index+i-5:index+i] + "..." + reference[index+i:index+i+20])
                        # print("---insertion! of len " + str(indelLen) + " at index=" + str(index+i))
                        insertions.append(insertTup)
                    else:
                        onceInsertions.append(insertTup)

                # check for deletion
                if read[i:i+5] == reference[index+i+indelLen:index+i+5+indelLen]:            
                    deleteTup = (reference[index+i:index+i+indelLen], index+i)
                    if deleteTup in onceDeletions:
                        # print("full read: " + read + " --- indel at: " + str(i))
                        # print("     read: " + read[i:i+20])
                        # print("     ref : " + reference[index+i-5:index+i] + "..." + reference[index+i:index+i+20])
                        # print("---deletion! of len " + str(indelLen) + " at index=" + str(index+i))
                        deletions.append(deleteTup)
                    else:
                        onceDeletions.append(deleteTup)

    insertions = list(set(insertions))
    deletions = list(set(deletions))
    # print("\nSNPS: "+str(snps))
    # print("\nINSERTIONS: "+str(insertions))
    # print("\nDELETIONS: "+str(deletions))

    output_fn = args.output_file
    zip_fn = output_fn + '.zip'
    with open(output_fn, 'w') as output_file:
        output_file.write('>' + args.output_header + '\n>SNP\n')
        for x in snps:
            output_file.write(','.join([str(u) for u in x]) + '\n')
        output_file.write('>INS\n')
        for x in insertions:
            output_file.write(','.join([str(u) for u in x]) + '\n')
        output_file.write('>DEL\n')
        for x in deletions:
            output_file.write(','.join([str(u) for u in x]) + '\n')
    with zipfile.ZipFile(zip_fn, 'w') as myzip:
        myzip.write(output_fn)
