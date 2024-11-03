#!/usr/bin/env python
import re

file = "/Users/carteralzamora/bioinfo/Bi624/Deduper-calzamora/fun_test.sam"


# def get_strand(sam_line: str) -> str:
#     '''This function will access the bitflag of a sam header and return the strandedness of the read as a + or -'''
#     rev_strand:bool = False 
#     spline = sam_line.split 
#     flag = int(spline[1])
#     if flag & 16 == 16:
#         rev_strand = True
#     elif flag & 16 != 16: 
#         rev_strand = False 
#     if rev_strand == True: 
#         print("-")
#         return("-")
    
# with open (file, "r") as fh1:
#     for sam_line in fh1:
#         rev_strand:bool = False 
#         # print(sam_line)
#         spline = sam_line.split()
#         # print(spline)
#         # print(spline[1])
#         flag = int(spline[1])
#         if flag & 16 == 16:
#             rev_strand = True
#         elif flag & 16 != 16: 
#             rev_strand = False 
#         if rev_strand == True: 
#             print("-")
#         # elif rev_strand == False:
#         #     print("+")

cigar_string = "2S6M2I1D3S"
pos = 10
cigar_hit = []
# def parse_cigar(cigar_string):
cigar_hit = re.findall(r'(\d+)([A-Z]{1})', cigar_string)
# print(matches)
pos_adj = 0 
for i, hit in enumerate(cigar_hit):
            #add match number to position adjust 
    if i == 0 and hit[1] == "S":
        pos_adj += int(hit[0])
        print(pos)
        print(pos_adj)
    new_pos = pos - pos_adj

print(pos)
print(new_pos)
            


# pos_adj = 0 
# for match in cigar_hit: 
#     if match[1] == "M": 
#         pos_adj += int(match[0])
#         print(match)
#     if match[1] == "D": 
#         pos_adj += int(match[0])
#         print(match)
# for i, match in enumerate(cigar_hit):
#     if i == 0:
#         pass
#     elif i != 0:
#         if match[1] == "S":
#             pos_adj += int(match[0])
#             print(match)
# print(pos_adj)

