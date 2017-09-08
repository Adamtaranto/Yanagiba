#!/usr/bin/env python
#yanagiba
#Version 1. Adam Taranto, August 2017
#Contact, Adam Taranto, adam.taranto@anu.edu.au

#############################################################################
# Filter and slice Nanopore reads which have been basecalled with Albacore. # 
# Takes fastq.gz and an Albacore summary file.                              #
#############################################################################

import argparse
import yanagiba as yb

def mainArgs():
		parser = argparse.ArgumentParser(
				description='Filter and slice Nanopore reads which have been basecalled with Albacore. Takes fastq.gz and an Albacore summary file.',
				prog='yanagiba')
		parser.add_argument('-i','--infile',
												type=str,
												required=True,
												default=None,
												help='Input fastq.gz file.')
		parser.add_argument('-s','--summaryfile',
												type=str,
												default=None,
												help='Albacore summary file with header row.')
		parser.add_argument('-o','--outfile',
												type=str,
												default="filtered.fastq.bgz",
												help='Write filtered reads to this file in .bgz format.')
		parser.add_argument('-l','--minlen',
												type=int,
												default=0,
												help='Exclude reads shorter than this length. Default: 0')
		parser.add_argument('-q','--minqual',
												type=int,
												default=10,
												help='Minimum quality score to retain a read. Default: 10')
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

def main():
	#Get args
	args = mainArgs()
	# Convert tail trim len to neg int if set.
	if args.tailtrim:
		tailtrim = args.tailtrim * -1
	# Preferentially source read information from summary file.
	if args.summaryfile:
		# Get names of reads which pass filter.
		keeplist = yb.getTargets(args.summaryfile,args.minlen,args.minqual)
		# Read in fastq.gz, keep records which passed filter and trim is required.
		yb.filterReads(args.infile,args.outfile,keeplist=keeplist,headtrim=args.headtrim,tailtrim=tailtrim,forceuniq=args.forceunique)
	else:
		# If no summary file provided, attempt to calculate quality scores directly from fastq using nanomath.
		yb.directFilter(args.infile,args.outfile,minqual=args.minqual,minlen=args.minlen,headtrim=args.headtrim,tailtrim=tailtrim,forceuniq=args.forceunique)