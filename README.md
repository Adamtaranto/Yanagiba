# Yanagiba

*A yanagiba is a japanese blade used for cutting sashimi slices. Albacore is a species of tuna. Puns.*

Yanagiba is used to filter short or low quality Oxford Nanopore reads which have been basecalled with 
Albacore. Takes fastq.gz and an Albacore summary file as input.

If no Albacore summary file is provided attempt to calculate mean qscore from directly from fastq file 
using [NanoMath](https://github.com/wdecoster/nanomath).
*Note:* Calculated quality scores appear to be lower for reads called with Metrichor, you may need to 
lower your minqual setting in this case.

# Table of contents

* [Getting started](#getting-started)
    * [Installing Yanagiba](#installing-yanagiba)
    * [Example usage](#example-usage)
* [Standard options](#standard-options)
* [License](#license)

## Getting started

### Installing Yanagiba

Install from PyPi:
```
pip install yanagiba
```

Clone and install from this repository:
```
git clone git@github.com:Adamtaranto/Yanagiba.git && cd Yanagiba && pip install -e .
```

### Example usage

**Input requirements:**

Albacore summary file must be tab delimited and have the header columns:  
  - "read_id"
  - "sequence_length_template"
  - "mean_qscore_template"

Unfiltered reads must be provided as fastq.gz file.

Extract reads from "albacoreReads.fastq.gz" and retain those with a quality score > 10 and 
length >= 1000bp. Finally, clip 50 bp from either end of the retained reads and write to 
"trimmedreads.fastq.bgz" 

```
yanagiba --minlen 1000 --headtrim 50 --tailtrim 50 --minqual 10 \
--summaryfile summary.txt \
--infile albacoreReads.fastq.gz \
--outfile trimmedreads.fastq.bgz
```

*Note:* Output files are in fastq.bgz compressed format. Unzip with:

```
gunzip -c trimmedreads.fastq.bgz > trimmedreads.fastq
```

## Standard options

Run `yanagiba --help` to view the program's most commonly used options:

```
Usage: yanagiba [-h] [-l MINLEN] [-q MINQUAL] [-s SUMMARYFILE] -i INFILE
                [-o OUTFILE] [--headtrim HEADTRIM] [--tailtrim TAILTRIM] [-u]

Filter and slice Nanopore reads which have been basecalled with Albacore.
Takes fastq.gz and an Albacore summary file.

Help:
  -h, --help            Show this help message and exit

Input options:
  -i, --infile          Input fastq.gz file.

  -s, --summaryfile     Albacore summary file with header row.

Output options:                 
  -o, --outfile         Write filtered reads to this file in .bgz format.

Settings:
  -l, --minlen          Exclude reads shorter than this length. 
                        (Default: 0)

  -q, --minqual         Minimum quality score to retain a read. 
                        (Default: 10)

  --headtrim            Trim x bases from begining of each read. 
                        (Default: 0)

  --tailtrim            Trim x bases from end of each read. 
                        (Default: None)

  -u, --forceunique     Enforce unique reads. Only store first instance of a
                        read from fastq input where readID occurs multiple
                        times. 
                        (Default: False)
```

## License

Software provided under MIT license.
