#!/usr/bin/env python3
from accessoryFunctions.accessoryFunctions import SetupLogging
from spadespipeline.primer_finder_bbduk import PrimerFinder
from argparse import ArgumentParser, RawTextHelpFormatter
import logging
__author__ = 'adamkoziol'


def test(args):
    from subprocess import call
    logging.info('Activate test mode')
    # Create a base command for pytest
    pytest_str = 'python -m pytest'
    # Append the appropriate arguments to the command
    if args.debug:
        pytest_str += ' -vv'
    if args.capture:
        pytest_str += ' -s'
    if args.maxfail:
        pytest_str += ' --maxfail={num}'.format(num=args.maxfail)
    # Include the --pyargs primer_finder to tell pytest to run the tests in the primer_finder package
    test_cmd = '{pytest} --pyargs primer_finder'.format(pytest=pytest_str)
    # Run the system call
    call(test_cmd, shell=True)


def run(args):
    # Run the script
    finder = PrimerFinder(path=args.path,
                          sequence_path=args.sequencepath,
                          primer_file=args.primerfile,
                          mismatches=args.mismatches,
                          kmer_length=args.kmerlength,
                          cpus=args.cpus,
                          analysistype='ePCR')
    # Run the script
    finder.main()
    logging.info('ePCR analyses complete')


def cli():
    parser = ArgumentParser(description='Perform in silico PCR using bbduk and SPAdes')
    subparsers = parser.add_subparsers(title='Title placeholder',
                                       description='Description placeholder',
                                       help='Sub-command help placeholder')
    # Create a parental parser from which the test and run subparsers can inherit --debug
    parent_parser = ArgumentParser(add_help=False)
    parent_parser.add_argument('-d', '--debug',
                               action='store_true',
                               help='Allow debug-level logging to be printed to the terminal')
    # Create a subparser to run the included unit tests
    test_subparser = subparsers.add_parser(parents=[parent_parser],
                                           name='test',
                                           help='Test help')
    test_subparser.add_argument('-s', '--capture',
                                action='store_true',
                                help='Print stdout from pytest to terminal')
    test_subparser.add_argument('--maxfail',
                                default=0,
                                type=int,
                                help='Exit after first num failures or errors. Default is 0 (will not exit prematurely')
    test_subparser.set_defaults(func=test)
    # Create a subparser to run the primer_finder script
    run_subparser = subparsers.add_parser(parents=[parent_parser],
                                          name='run',
                                          formatter_class=RawTextHelpFormatter,
                                          help='Run help')
    run_subparser.add_argument('-p', '--path',
                               required=True,
                               help='Specify directory in which reports are to be created')
    run_subparser.add_argument('-s', '--sequencepath',
                               required=True,
                               help='Path of folder containing .fasta/.fastq(.gz) files to process.')
    run_subparser.add_argument('-n', '--cpus',
                               default=0,
                               help='Number of threads. Default is the number of cores in the system')
    run_subparser.add_argument('-pf', '--primerfile',
                               required=True,
                               help='Absolute path and name of the primer file (in FASTA format) to test. The file\n'
                                    'must have every primer on a separate line AND -F/-R following the name e.g.\n'
                                    '>primer1-F\n'
                                    'ATCGACTGACAC....\n'
                                    '>primer1-R\n'
                                    'ATCGATCGATCGATG....\n'
                                    '>primer2-F\n'
                                    '.......\n')
    run_subparser.add_argument('-m', '--mismatches',
                               default=1,
                               choices=[0, 1, 2, 3],
                               help='Number of mismatches allowed [0-3]. Default is 1')
    run_subparser.add_argument('-k', '--kmerlength',
                               default='55,77,99,127',
                               help='The range of kmers used in SPAdes assembly. Default is 55,77,99,127, but you can\n'
                                    'provide a comma-separated list of kmers e.g. 21,33,55,77,99,127 or a\n'
                                    'single kmer e.g. 33')
    run_subparser.set_defaults(func=run)
    # Get the arguments into an object
    arguments = parser.parse_args()
    # Run the appropriate function for each sub-parser.
    try:
        SetupLogging(debug=arguments.debug)
        arguments.func(arguments)
    # If not sub-parser specified, print the help
    except AttributeError as e:
        print(e)
        parser.parse_args(['-h'])


if __name__ == '__main__':
    cli()
