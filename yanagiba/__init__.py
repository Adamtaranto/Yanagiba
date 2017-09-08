#!/usr/bin/env python
#yanagiba
#Version 1. Adam Taranto, August 2017
#Contact, Adam Taranto, adam.taranto@anu.edu.au

#############################################################################
# Filter and slice Nanopore reads which have been basecalled with Albacore. # 
# Takes fastq.gz and an Albacore summary file.                              #
#############################################################################
import gzip
import pandas
from Bio import SeqIO, bgzf
from nanomath import aveQual

def getTargets(summaryfile,minlen,minqual):
	df = pandas.read_csv(summaryfile, sep='\t', header=0)
	keep = df.ix[(df['sequence_length_template'] >= minlen) & (df['mean_qscore_template'] >= minqual)]
	keeplist = keep['read_id'].tolist()
	return keeplist

def directFilter(infile,outfile,minqual=0,minlen=0,headtrim=None,tailtrim=None,forceuniq=False):
	seen = list()
	total = 0
	with gzip.open(infile, "rt") as handle, bgzf.BgzfWriter(outfile, "wb") as output_handle:
		for record in SeqIO.parse(handle, "fastq"):
			total += 1
			if aveQual(record.letter_annotations["phred_quality"]) > minqual and len(record) > minlen:
				if not forceuniq:
					seen.append(record.id)
					SeqIO.write(record[headtrim:tailtrim], handle=output_handle, format="fastq")
				elif (forceuniq and record.id not in seen):
					seen.append(record.id)
					SeqIO.write(record[headtrim:tailtrim], handle=output_handle, format="fastq")
	print("Saved %s records out of %s records seen." % (len(seen),str(total)) )

def filterReads(infile,outfile,keeplist=None,headtrim=None,tailtrim=None,forceuniq=False):
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