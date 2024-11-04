#!/usr/bin/env python
import re

file = "/Users/carteralzamora/bioinfo/Bi624/Deduper-calzamora/STL96.txt"
sam_line = "NS500451:154:HWKTMBGXX:1:11101:18996:1145:TTCGCCTA	0	2	10	36	2S6M2I1D3S"


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
        # else:
        #     #if there is no soft 5' clipping do not adjust the start position 
        #     new_pos = pos
    # if the match is on the reverse strand 
    if rev_strand == True: 
        pos_adj = 0 
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

# print(get_5_start_pos("NS500451:154:HWKTMBGXX:1:11101:18996:1145:TTCGCCTA	16	2	10	36	2S6M2I1D3S"))

def get_line_info(sam_line: str) -> tuple:
    '''This function will take in a sam file line and return a touple containing
    [true 5' start position, strand, UMI]'''
    line_info = ()
    start_pos = get_5_start_pos(sam_line)
    strand = reverse_strand(sam_line)
    spline = sam_line.split()
    UMI = spline[0].split(":")
    UMI = UMI[7]
    line_info = (start_pos, strand, UMI)
    return(line_info)

print(get_line_info(sam_line))

umi_set = set()
with open(file) as fh1:
    for umi in fh1:
        umi = umi.strip()
        umi_set.add(umi)

print(umi_set)
