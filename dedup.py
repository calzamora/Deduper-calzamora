#!/usr/bin/env python

## this scropt will remove all ocr duplicates from a double stranded fastqc file 
##while leaving all real biological duplicates 

import argparse
import re

def get_args():
    parser = argparse.ArgumentParser(description="deuper script")
    parser.add_argument("-f", help="sorted SAM input file ", type = str) #type: str
    parser.add_argument("-o", help="output SAM file name ", type = str) #type: str
    parser.add_argument("-u", help="list of known umis", type = str) #type: str
    ###add -h help message 

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
with (open(in_file, "r") as in_file,
      open(out_file, "w") as out_file):
    
    while True: 
        sam_line = in_file.readline().strip()
        if sam_line == "":
            break 
        spline = sam_line.split()

        #write out all the header lines: 
        if len(spline[0]) == 3:
            # print(spline[0])
            out_file.write(f"{sam_line}\n")
        elif len(spline[0]) != 3:
            #check if UMI is known: 
            # print(spline[0])
            umi = spline[0].split(":")
            umi = umi[-1]
            # print(umi)
            if umi not in umi_set:
                continue
            elif umi in umi_set:
                line_info = get_line_info(sam_line)
                chrom = line_info[0]
            
            #when i hit a new chromosome, wipe the set and reset chr_num variable to current chrom:
            if chrom != chr_num:
                print(unique_set)
                # print(sam_line)
                # print(chrom)
                # print(chr_num)
                dup_set = set()
                chr_num = chrom 
                unique_set.add(line_info)
                out_file.write(f"{sam_line}\n")

            
            #on the same chromosome check if the line info is unique and if so write out and save to set
            elif chrom == chr_num:
                if line_info not in unique_set:
                    unique_set.add(line_info)
                    out_file.write(f"{sam_line}\n")
                elif line_info in unique_set:
                    pass





