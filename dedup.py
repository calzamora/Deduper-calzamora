#!/usr/bin/env python

## this scropt will remove all ocr duplicates from a double stranded fastqc file 
##while leaving all real biological duplicates 

import argparse
import re

def get_args():
    parser = argparse.ArgumentParser(description="INPUT: dedup.py -f [sorted input sam file - no paired end] \
                          -o [output sam file] -u [known UMI list] | OUTPUT: sorted sam file containing only biological duplicates, statistics printed to standard out")
    parser.add_argument("-f", help="sorted SAM input file ", type = str) #type: str
    parser.add_argument("-o", help="output SAM file name ", type = str) #type: str
    parser.add_argument("-u", help="list of known umis", type = str) #type: str


    return parser.parse_args()

args = get_args()

in_file = args.f
out_file = args.o 
umis = args.u  
cigar_hit = []

### check strandedness function 
def reverse_strand(sam_line: str) -> bool:
    '''This function will access the bitflag of a sam header and return 
    True if reverse, False if foward strand'''
    spline = sam_line.split()
    flag = int(spline[1])
    if flag & 16 == 16:
        return True
    else: 
        return False 


def get_5_start_pos(sam_line: str) -> int:
    '''This function will take access the cigar string and position of a sam header 
    and return the adjusted 5' start position '''
    spline = sam_line.split()
    pos = int(spline[3])
    cigar = spline[5]
    clip_num = str("0")
    rev_strand:bool = reverse_strand(sam_line)
    #if the read is on the + strand, just adjust for left soft clipping
    if rev_strand == False:
        cigar_hit = re.findall(r'(\d+)([A-Z]{1})', cigar)
        # print(matches)
        pos_adj = 0 
        for i, hit in enumerate(cigar_hit):
            #if the first index position of the cigar string is an S 
            if i == 0 and hit[1] == "S":
                #set position adjust = to the integer of soft clipping
                pos_adj += int(hit[0])
            #subtract the soft clipping from the given position to get the true 5' start position 
            new_pos = pos - pos_adj
    # if the match is on the reverse strand 
    if rev_strand == True: 
        pos_adj = 0 
        #create tuple holding the letter and corresponding number 
        cigar_hit = re.findall(r'(\d+)([A-Z]{1})', cigar)
        for hit in cigar_hit:
            #add match number to position adjust 
            if hit[1] == "M":
                pos_adj += int(hit[0])
            #add deletion number to  position adjust
            if hit[1] == "D":
                pos_adj += int(hit[0])
            # adjust for N for deletions 
            if hit[1] == "N":
                pos_adj += int(hit[0])
        for i, hit in enumerate(cigar_hit):
            #if it's 3' clipping, skip
            if i == 0:
                pass
            #if it's 5' clipping, add to the position adjust 
            elif i != 0:
                if hit[1] == "S":
                    pos_adj += int(hit[0])
        #
        new_pos = pos + pos_adj
    return(new_pos)


def get_line_info(sam_line: str) -> tuple:
    '''This function will take in a sam file line and return a touple containing
    [chrom, true 5' start position, strand, UMI]'''
    line_info = ()
    start_pos = get_5_start_pos(sam_line)
    strand = reverse_strand(sam_line)
    spline = sam_line.split()
    UMI = spline[0].split(":")
    UMI = UMI[-1]
    chrom = spline[2]
    line_info = (chrom, start_pos, strand, UMI)
    return(line_info)

#create set of UMIS: 
umi_set = set()
with open(umis) as fh1:
    for umi in fh1:
        umi = umi.strip()
        umi_set.add(umi)

### start flow that will loop by CHROMOSOME: 
#initialize set that will hold unique reads: 
unique_set = set()
chr_num = str("1")
pcr_dups_removed = 0 
bio_dupes_kept = 0 
unknown_umis = 0 

total_pcr_dups_removed = 0 
total_bio_dupes_kept = 0 
total_unknown_umis = 0 

with (open(in_file, "r") as in_file,
      open(out_file, "w") as out_file):
    
    while True: 
        sam_line = in_file.readline().strip()
        if sam_line == "":
            # #at the end of the file print out total counts and end 
            # print(f"Total PCR duplicates removed: {total_pcr_dups_removed}") 
            # print(f"Total Biological duplicates written out: {total_bio_dupes_kept}")
            # print(f"Total Unknown UMIs removed: {total_unknown_umis}")
            break 
        spline = sam_line.split()

        #write out all the header lines: 
        if len(spline[0]) == 3:
            out_file.write(f"{sam_line}\n")
        elif len(spline[0]) != 3:
            #check if UMI is known: 
            umi = spline[0].split(":")
            umi = umi[-1]
            if umi not in umi_set:
                #count the total and per chromosome unknown umis
                unknown_umis += 1
                continue
            elif umi in umi_set:
                line_info = get_line_info(sam_line)
                chrom = line_info[0]
            
            #when i hit a new chromosome, wipe the set and reset chr_num variable to current chrom:
            if chrom != chr_num:
                #print out per chromosome stats and reset for next loop 
                # print(f"Chromosome Numbeer {chr_num}: PCR duplicates removed: {pcr_dups_removed}") 
                print(f"{chr_num}   {bio_dupes_kept}")
                # print(f"Chromosome Numbeer {chr_num}: Unknown UMIs removed: {unknown_umis}")
                total_pcr_dups_removed += pcr_dups_removed
                total_bio_dupes_kept += bio_dupes_kept
                total_unknown_umis += unknown_umis
                pcr_dups_removed = 0 
                bio_dupes_kept = 0 
                unknown_umis = 0   
                dup_set = set()
                chr_num = chrom 
                unique_set.add(line_info)
                #write out the first read we see 
                out_file.write(f"{sam_line}\n")

            
            #on the same chromosome check if the line info is unique and if so write out and save to set
            elif chrom == chr_num:
                if line_info not in unique_set:
                    unique_set.add(line_info)
                    #iterate counters 
                    bio_dupes_kept += 1
                    #write out sam line 
                    out_file.write(f"{sam_line}\n")
                elif line_info in unique_set:
                    #iterate counters 
                    pcr_dups_removed += 1
                    pass





