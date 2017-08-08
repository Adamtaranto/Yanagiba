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
from Bio import SeqIO, bgzf
import pandas

def getTargets(summaryfile,minlen,minqual):
	df = pandas.read_csv(summaryfile, sep='\t', header=0)
	keep = df.ix[(df['sequence_length_template'] >= minlen) & (df['mean_qscore_template'] >= minqual)]
	keeplist = keep['read_id'].tolist()
	return keeplist

def filterReads(infile,outfile,keeplist,headtrim,tailtrim,forceuniq=False):
	seen = list()
	with gzip.open(infile, "rt") as handle, bgzf.BgzfWriter(outfile, "wb") as output_handle:
		for record in SeqIO.parse(handle, "fastq"):
			if record.id in keeplist:
				if not forceuniq:
					SeqIO.write(record[headtrim:tailtrim], handle=output_handle, format="fastq")
				elif (forceuniq and record.id not in seen):
					seen.append(record.id)
					SeqIO.write(record[headtrim:tailtrim], handle=output_handle, format="fastq")
	if forceuniq:
		print("Saved %s unique records from %s filtered records." % (len(seen),len(keeplist)))

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
												default="filtered.fastq.bgz",
												help='Write filtered reads to this file in .bgz format.')
		parser.add_argument('--headtrim',
												type=int,
												default=0,
												help='Trim x bases from begining of each read. Default: 0')
		parser.add_argument('--tailtrim',
												type=int,
												default=None,
												help='Trim x bases from end of each read. Default: None')
		parser.add_argument('-u','--forceunique',
												action='store_true',
												default=False,
												help='Enforce unique reads. Only store first instance of a read from fastq input where readID occurs multiple times.')
		args = parser.parse_args()
		return args

def main(args):
	# Convert tail trim len to neg int if set
	if args.tailtrim:
		tailtrim = args.tailtrim * -1
	# Get names of reads which pass filter
	keeplist = getTargets(args.summaryfile,args.minlen,args.minqual)
	# Read in fastq.gz, keep records which passed filter and trim is required
	filterReads(args.infile,args.outfile,keeplist,args.headtrim,tailtrim,forceuniq=args.forceunique)

if __name__== '__main__':
	args = mainArgs()
	main(args)