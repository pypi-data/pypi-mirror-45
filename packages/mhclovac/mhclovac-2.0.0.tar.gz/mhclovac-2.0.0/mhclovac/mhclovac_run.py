#!usr/bin/env python
"""Entry point for mhclovac"""

import sys
from mhclovac.misc import *
from mhclovac.argument_parser import parse_args


def worker(sequence, seq_name, args, output):

    sequence = str(sequence).upper()
    seq_name = str(seq_name)

    models_dict = load_models()
    standardizer, regressor = models_dict[args.hla]

    for i in range(len(sequence) - args.peptide_length + 1):
        peptide = sequence[i: i+args.peptide_length]

        X = get_feature_vector(peptide)
        X = standardizer.transform(X)
        score = regressor.predict(X)[0]
        total_score = np.power(10, score)

        line = '\t'.join([seq_name, args.hla, peptide, str(total_score)])
        output.write(line + '\n')
    return


def run():
    args = parse_args(sys.argv[1:])
    output = open(args.output, 'w') if args.output else sys.stdout

    if args.print_header:
        print_header(output)

    if args.fasta:
        for seq_name, sequence in fasta_reader(args.fasta):
            worker(sequence, seq_name, args, output)

    elif args.sequence:
        seq_name = args.sequence_name or 'unknown'
        worker(args.sequence, seq_name, args, output)

    else:
        raise RuntimeError('Must provide sequence or fasta file')


def main():
    # Entry point for mhclovac
    sys.exit(run())
