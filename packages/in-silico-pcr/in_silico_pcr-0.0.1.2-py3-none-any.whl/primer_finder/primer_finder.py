#!/usr/bin/env python3
from accessoryFunctions.accessoryFunctions import SetupLogging
from spadespipeline.primer_finder_bbduk import PrimerFinder
from argparse import ArgumentParser
import logging
import time
__author__ = 'adamkoziol'


def cli():
    parser = ArgumentParser(description='Perform in silico PCR using bbduk and SPAdes')
    parser.add_argument('-p', '--path',
                        required=True,
                        help='Specify directory in which reports are to be created')
    parser.add_argument('-s', '--sequencepath',
                        required=True,
                        help='Path of folder containing .fasta/.fastq(.gz) files to process.')
    parser.add_argument('-n', '--cpus',
                        help='Number of threads. Default is the number of cores in the system')
    parser.add_argument('-pf', '--primerfile',
                        required=True,
                        help='Absolute path and name of the primer file (in FASTA format) to test. The file must have'
                             'every primer on a separate line AND -F/-R following the name e.g. '
                             '>primer1-F\n'
                             'ATCGACTGACAC....\n'
                             '>primer1-R\n'
                             'ATCGATCGATCGATG....\n'
                             '>primer2-F\n'
                             '.......\n')
    parser.add_argument('-m', '--mismatches',
                        default=1,
                        help='Number of mismatches allowed [0-3]. Default is 1')
    parser.add_argument('-k', '--kmerlength',
                        default='55,77,99,127',
                        help='The range of kmers used in SPAdes assembly. Default is 55,77,99,127, but you can '
                             'provide a comma-separated list of kmers e.g. 21,33,55,77,99,127 or a single kmer e.g. 33')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Allow debug-level logging to be printed to the terminal')
    # Get the arguments into an object
    arguments = parser.parse_args()
    arguments.pipeline = False
    SetupLogging(debug=arguments.debug)
    # Define the start time
    arguments.start = time.time()

    # Run the script
    finder = PrimerFinder(args=arguments,
                          analysistype='ePCR')
    # Run the script
    finder.main()
    logging.info('ePCR analyses complete')


if __name__ == '__main__':
    cli()
