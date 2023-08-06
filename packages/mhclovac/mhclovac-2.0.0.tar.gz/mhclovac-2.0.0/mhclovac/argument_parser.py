import argparse

mhclovac_description = """
mhclovac - MHC binding prediction based on modeled physicochemical 
properties of peptides. Version: 1.0.1. Author: Stefan Stojanovic
"""


def parse_args(argv):
    parser = argparse.ArgumentParser(description=mhclovac_description)
    parser.add_argument('--sequence', type=str, help='Input sequence')
    parser.add_argument('--sequence_name', type=str, help='Sequence name')
    parser.add_argument('--fasta', type=str, help='FASTA file')
    parser.add_argument('--hla', type=str, help='HLA type', required=True)
    parser.add_argument('--peptide_length', type=int, help='Peptide length',
                        required=True)
    parser.add_argument('--output', type=str,
                        help='Output file. If not provided output will be '
                             'written to stdout')
    parser.add_argument('--print_header', action='store_true',
                        help='Print column names')
    return parser.parse_args(argv)
