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
        for char in cigar:
            #if its soft clipping, add the clipping number to the start position 
            if char == "S":
                pos = pos + int(clip_num)
            if char == "M":
                pos = pos
            #if the character is an integer, add the clip number to the char 
            else: 
                clip_num + char
    # if the match is on the reverse strand 
    if rev_strand == True: 
        pos_adj = 0 
        cigar_hit = re.findall(r'(\d+)([A-Z]{1})', cigar)
        for hit in cigar_hit:
            #add match number to position adjust 
            if hit[1] == "M":
                pos_adj += int(hit[0])
            if hit[1] == "D":
                pos_adj += int(hit[0])
        for i, hit in enumerate(cigar_hit):
            if i == 0:
                pass
            elif i != 0:
                if hit[1] == "S":
                    pos_adj += int(hit[0])
        pos = pos + pos_adj
    return(pos)

