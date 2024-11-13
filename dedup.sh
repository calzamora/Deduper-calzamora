#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH -c 10
#SBATCH --mem=100G 

/usr/bin/time -v \
    ./dedup.py \
    -f /projects/bgmp/calz/bioinfo/Bi624/Deduper-calzamora/sorted_cca.sam \
    -u /projects/bgmp/calz/bioinfo/Bi624/Deduper-calzamora/STL96.txt \
    -o rerun_dedup.sam 