# Deduper 
## Carter Alzamora | 11 November 2024

### The probelm:
Remove PCR duplicate alignments from a sorted sam file but keep Biological duplicates.

**Metrics:**\
Chromosome #: Same for both duplicates\
5' Start Position: Same for both duplicates\
Strand: Same for both dublicates\
UMI: different = bio dup | same = PCR dup 

**Soft Clipping:**\
Plus strand:
Subtract:\
LEFT MOST soft clipping from cigar strand. | S

Minus strand:\
Add:\
Right most soft clipping | S\
Deletions | D\
Skipped Region | N\
Matches | M

### Test Files: 
Cases to keep: 
1. Biological Duplicates: same chrom #, position #, strandedness, DIFFERENT UMI 
2. Not real duplicates: everything the same but position is different after adjusting for soft clipping 
3. everything the same except for: chromosome #, OR position #, OR strand OR UMI 

Cases to remove:
1. PCR duplicates: all identical same chrom #, position #, strandedness, same UMI
2. different starting position before adjusting pos based on soft clipping, same after adjusting 
3. incorrect UMI 

LINE 25: initial read KEEP  
LINE 26: identical Biological dup KEEP\
LINE 27:duplicate after soft clipping REMOVE\
LINE 28:looks like dup but isn't after soft clipping KEEP\
LINE 29:looks like duplicate but not on same strand KEEP\
LINE 30: looks like duplicate but not on same chrom KEEP\
LINE 32: unknown UMI REMOVE

### Script Writing: 

function for strandedness MUST be ahead of function to adjust for soft clipping.

all functions for getting chrom, strand, 5' start, and umi must defined ahead of get_line_info 

saving to memory by chromosome seems to work for saving space. 

### Testing: 
create sorted sam file: 
samtools view -u /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam | samtools sort | samtools view -h > sorted_cca.sam

My test files are correctly deduping! 

test on Wes' Yes! 

check numbers: 
grep -v "^@" Datast1_deduped.sam | cut -f 3 | sort -g | uniq -c

slurm out: 
1   697508
10   564902
11   1220388
12   359950
13   467658
14   387238
15   437464
16   360922
17   517565
18   290505
19   571664
2   2787017
3   547614
4   589838
5   562159
6   510817
7   1113182
8   576462
9   627487
MT   202001
X   317852
Y   2246
JH584299.1   2
GL456233.2   655
GL456211.1   5
GL456221.1   3
GL456354.1   0
GL456210.1   4
GL456212.1   3
JH584304.1   293
GL456379.1   1
GL456367.1   2
GL456239.1   0
GL456383.1   0
MU069435.1   5449
GL456389.1   0
GL456370.1   20
GL456390.1   0
GL456382.1   0
GL456396.1   16
GL456368.1   2
MU069434.1   2

MEMORY: 	Maximum resident set size (kbytes): 3166748\
TIME: 	Elapsed (wall clock) time (h:mm:ss or m:ss): 1:50.41