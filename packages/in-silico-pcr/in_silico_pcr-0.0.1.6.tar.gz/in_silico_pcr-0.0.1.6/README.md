## Description

This tool is an attempt to do _in silico_ PCRs from .fastq(.gz) or .fasta files. 

The script uses bbduk to bait reads containing the primer sequences from the .fastq(.gz) files. It 
performs a second round of baiting on the original .fastq(.gz) files with the newly created baited
.fastq files in order to hopefully have sequence data to span the entire amplicon. Resulting
double-baited read files are assembled into contigs using SPAdes. 
The assemblies are BLASTed against the primer file to determine if both forward and reverse 
primers can be found in a single contig, thus a valid PCR product. PCR product length is also 
reported.

The longer the reads in the fastq file(s), the better the assembly and the fewer false negatives.

## External Dependencies
1. conda


## Installation

`conda install -c adamkoziol in_silico_pcr`

## Inputs

1. Primer pair list (fasta). Primer names have to end with “-F” or “-R”. Note: it is possible to have an integer 
following the direction: >vtx1a-F1 or >vtx1a-F are both acceptable
2. Raw reads (FASTQ) or assemblies (FASTA)

## Usage

Typical command line usage:
````
primer_finder.py run -p ABSOLUTE PATH TO FOLDER IN WHICH REPORTS FOLDER TO BE CREATED -s ABSOLUTE PATH TO SEQUENCE FILES 
-p ABSOLUTE PATH AND NAME OF PRIMER FILE
````

### Optional arguments

`-m NUMBER OF MISMATCHES`
`-n number of threads`


## Test Dataset

I've provided six genomes in a mixture of FASTA and FASTQ formats to use to test the script on your system. 
The FASTA files are assemblies, while the FASTQ files are pre-baited files to reduce size. 
The report you create should match the one in the 'desired_outputs' folder (there may be small
differences when it comes to the order of genes).

NOTE: Please use absolute paths when running the program. If you don't there will probably be 
errors right at the beginning.

````
primer_finder.py test -s -d
````

Note that in the provided ePCR.csv report file, in the results for _eae_ there are  four genome 
locations rather than the expected two. This is due to the fact that there are two separate 
primer sets for _eae_. This is fine for this output, but if you don't want results like this 
make sure that the names of the primers are unique.

Additionally, for 2014-SEQ-0121, the FASTQ and FASTA files yield different number of genes. The FASTQ sample has an
additional gene, _vtx2c_, this is likely due to issues with the assembly that do not always appear when
assembling with the double-baited reads (the de Bruijn graphs should be much simpler). 

## Options

````

usage: primer_finder_bbduk.py [-h] -s SEQUENCEPATH [-n CPUS] -p PRIMERFILE
                              [-m MISMATCHES]
                              path

Perform in silico PCR using bbduk and SPAdes

positional arguments:
  path                  Specify output directory

optional arguments:
  -h, --help            show this help message and exit
  -s SEQUENCEPATH, --sequencepath SEQUENCEPATH
                        Path of folder containing .fasta/.fastq(.gz) files to
                        process.
  -n CPUS, --cpus CPUS  Number of threads. Default is the number of cores in
                        the system
  -p PRIMERFILE, --primerfile PRIMERFILE
                        Absolute path and name of the primer file (in FASTA
                        format) to test. The file must haveevery primer on a
                        separate line AND -F/-R following the name e.g.
                        >primer1-F 
                        ATCGACTGACAC.... 
                        >primer1-R
                        ATCGATCGATCGATG.... 
                        >primer2-F 
                        .......
  -m MISMATCHES, --mismatches MISMATCHES
                        Number of mismatches allowed [0-3]. Default is 0

````
