#!/usr/bin/env python
#python 2.7.5
#yanagiba.py
#Version 1. Adam Taranto, August 2017
#Contact, Adam Taranto, adam.taranto@anu.edu.au

#############################################################################
# Filter and slice Nanopore reads which have been basecalled with Albacore. # 
# Takes fastq.gz and an Albacore summary file.                              #
#############################################################################

import argparse
import gzip
from Bio import SeqIO
import pandas

def getTargets(summaryfile,minlen,minqual):
	df = pandas.read_csv(summaryfile, sep='\t', header=0)
	keep = df.ix[(df['sequence_length_template'] >= minlen) & (df['mean_qscore_template'] >= minqual)]
	keeplist = keep['read_id'].tolist()
	return keeplist

def filterReads(infile,outfile,keeplist,headtrim,tailtrim):
	output_handle = open(outfile,"w")
	with gzip.open(infile, "rt") as handle:
		for record in SeqIO.parse(handle, "fastq"):
			if record.id in keeplist:
				SeqIO.write(record[headtrim:tailtrim], output_handle, "fastq")
	output_handle.close()

def mainArgs():
		parser = argparse.ArgumentParser(
				description='Filter and slice Nanopore reads which have been basecalled with Albacore. Takes fastq.gz and an Albacore summary file.',
				prog='yanagiba')
		parser.add_argument('-l','--minlen',
												type=int,
												default=0,
												help='Exclude reads shorter than this length. Default: 0')
		parser.add_argument('-q','--minqual',
												type=int,
												default=10,
												help='Minimum quality score to retain a read. Default: 10')
		parser.add_argument('-s','--summaryfile',
												type=str,
												required=True,
												default=None,
												help='Albacore summary file with header row.')
		parser.add_argument('-i','--infile',
												type=str,
												required=True,
												default=None,
												help='Input fastq.gz file.')
		parser.add_argument('-o','--outfile',
												type=str,
												default="filtered.fastq",
												help='Write filtered reads to this file.')
		parser.add_argument('--headtrim',
												type=int,
												default=0,
												help='Trim x bases from begining of each read. Default: 0')
		parser.add_argument('--tailtrim',
												type=int,
												default=None,
												help='Trim x bases from end of each read. Default: None')
		args = parser.parse_args()
		return args

def main(args):
	# Convert tail trim len to neg int if set
	if args.tailtrim:
		tailtrim = args.tailtrim * -1
	# Get names of reads which pass filter
	keeplist = getTargets(args.summaryfile,args.minlen,args.minqual)
	# Read in fastq.gz, keep records which passed filter and trim is required
	filterReads(args.infile,args.outfile,keeplist,args.headtrim,tailtrim)

if __name__== '__main__':
	args = mainArgs()
	main(args)