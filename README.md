# Yanagiba

*A yanagiba is a japanese blade used for cutting sashimi slices. Albacore is a species of tuna. Puns.*

Yanagiba is used to filter short or low quality Oxford Nanopore 
reads which have been basecalled with Albacore.
Takes fastq.gz and an Albacore summary file as input.

**Input requirements:**

Albacore summary file must be tab delimited and have the header columns:  
  - "read_id"
  - "sequence_length_template"
  - "mean_qscore_template"

Unfiltered reads must be provided as fastq.gz file.

**Example usage:**

Extract reads from "albacoreReads.fastq.gz" and retain those with 
a quality score > 10 and length >= 1000bp. 
Finally, clip 50 bp from either end of the retained reads and write to "trimmedreads.fastq" 

`
./yanagiba.py --minlen 1000 --headtrim 50 --tailtrim 50 --minqual 10 \
--summaryfile summary.txt \
--infile albacoreReads.fastq.gz \
--outfile trimmedreads.fastq
`