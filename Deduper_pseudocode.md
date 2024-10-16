# Deduper Pseudocode 

## Functions: 

### arg_parse(-u --umi_list, -f --sam_file, -o --out_file, -h --help)
```
this function will take in:

-f sorted sam file
-o output deduplicated sam file 
-u list of known umis 
-h output a useful help message 
```

### get_line_info(sam_line):
```
```this function will take in a sam file line and return an array containing: [Position adjusted for soft clipping, strandedness, UMI]```

chromosome # : index position in line 
pos # : de_softclip 
strand : check_strand
UMI : index position in line
    if strand = - 
    rev_comp UMI 

###NOTE IF STRAND IS - REV COMP UMI 

return[position #, strand, UMI]
```

### check_strand(sam_line):
```
```This function will take in the sam line and parse the bit flag at bit 16 to return the strandedness```
if bflag & 16 == 16:
    rev_comp = True
else
    rev comp = False 

return[+ OR -]
```

### de_softclip(sam_line):
```
```This function will take in the sam line and return the position adjusted for soft clipping```
#initial position not adjusted for soft clipping: 
pos = int(sam_line[3])
cig_string = sam_line[5]

for char in cig_string:
    if letter = 's'
        pos = pos + int(clip_num)
    if letter = 'm' 
        pos = pos 
    else: 
        clip_num.append(char)

return(pos)
```

## Flow:
```
#initialize duplicate set that will hold the position, strandedness, and UMI 
dup_set = {}

#this variable will be what we use to loop over the file and save to the dupe set BY chromosome 
chr_num = 1

#initialize known umi set 
umi_set = {}
with open(umi_list_file, 'r') as umi_list:
    for umi in umi_list:
        umi_set.add(umi)
        rev_comp_umi = reverse complement of every UMI 
        umi_set.add(rev_comp_umi)

with open(sam_file, "r") as in_file, 
     open(out_file, "w" ) as out_file:

    

    while True: 
        sam_line = in_file.readline.strip()
        sam_line = sam_line.split()
        umi = sam_line.split(":")[8]
        chrom = sam_line[0]

        #write out headers (all start with @)
        if sam_line[0] = "@"
            out_file.write(sam_line)
        else same_line[0] != "@"

            #check if umi is in known set:
            if umi not in umi_set: 
                continue 
            else if umi in umi_set: 
                line_info = get_line_info(sam_line)
                chrom = line_info[0]
            
            #when you hit a new chromosome, wipe the set and set chr_num variable to current chromosome: 
            if chrom != chr_num:
                dup_set = {}
                chr_num = chrom
            
            #if the combination of the chromosome #, position, strand, and UMI are UIQUE save to dup_set and write to out file: 
            if line_info not in dup_set:
                dup_set.add(line_info)
                out_file.write(line_info)
            elif line_info in dupe_set:
                pass 

```