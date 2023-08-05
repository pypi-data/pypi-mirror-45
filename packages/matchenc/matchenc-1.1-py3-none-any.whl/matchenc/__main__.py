'''
A script to identify the encoding used inp a file, if unspecified.
'''

import argparse, logging
from matchenc import matchenc

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='[%(levelname)8s]: %(message)s')
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-i', '--infile', help='input file', required=True)
    PARSER.add_argument('--exp', help='expected terms (separate terms by a space)',
                        default=[], nargs='*', action='store')
    ARGS = PARSER.parse_args()
    
    matchenc(ARGS.infile, ARGS.exp)
