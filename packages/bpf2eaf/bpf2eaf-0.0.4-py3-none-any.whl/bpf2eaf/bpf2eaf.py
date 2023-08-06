#!/bin/python
#
#
# Script that converts bpf files to eaf files. If they do not exist,
# they are newly created. If the output file does already exist,
# the content of the output is added to the existing one.
#
# Exit codes can be found in ErrorCodesBPF2EAF.py
#
#

import argparse
import time
from BPFParser import BPFParser
from . import ErrorCodesBPF2EAF

parser = argparse.ArgumentParser(description='BPF to EAF conversion.')

parser.add_argument('-i', '--bpf', dest='bpf', required=True,
                    help='Input BPF file that should be converted.')

parser.add_argument('-s', '--signal', dest='signal', required=True,
                    help='Input signal wav file.')

parser.add_argument('-o', '--eaf', dest='eaf', required=True,
                    help='Output EAF file.')

parser.add_argument('-l', '--language', dest='language', required=True,
                    help='The language to set in the EAF file.')

parser.add_argument("-k", "--knownissues", dest='knownIssues', action='store_true', default=False,
                    help='Prints information about the known issues, only works if bpf, signal and output are '+
                         'specified. Will pause 5 seconds after printing the known issues.')

args = None
try:
    args = parser.parse_args()
except:
    parser.print_help()
    quit(ErrorCodesBPF2EAF.ERROR_CODE_NOT_ENOUGH_CMD_ARGUMENTS)
#print(args.accumulate(args.integers))


knownIssues = "- only supports ORT, KAN, MAU, and TRN tier\n"
# knownIssues += "- TRN tier handling doesn't work correctly as it can contain white spaces (only 1st word " \
# "is extracted)\n"

if args.knownIssues:
    print("----------------- Known Issues -----------------------")
    print(knownIssues)
    time.sleep(5)

#parser.print_help()

#print("Input:  " + args.bpf)
#print("Output: " + args.eaf)

# bpfParser = BPFParser(sampleRate=16000, topLevelTier = "ORT:", tiersToProcess = ["ORT:", "KAN:"])
bpfParser = BPFParser(sampleRate=16000, signalLocation=args.signal, topLevelTier="ORT:")
bpfParser.readBPFFile(args.bpf)
bpfParser.convertToEAF(args.eaf, ling=args.language)

