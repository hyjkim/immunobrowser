#!/usr/bin/env python
import argparse



parser = argparse.ArgumentParser(description="Placeholder for pubBlast executible")
parser.add_argument('fasta', type=str, help="input fasta for blast")
parser.add_argument('report', type=str, help="output file location")

args = parser.parse_args()

file = open(args.report, 'w')
file.write('Placeholder report for %s' % (args.fasta))
