# Untuk menggabungkan keseluruhan operasi BPCS yang telah dibuat

import os.path
import argparse

from bpcs_steg_decode import decode
from bpcs_steg_encode import encode
from bpcs_steg_capacity import capacity
from bpcs_steg_test import test_all

parser = argparse.ArgumentParser()

valid_opt_behaviors = {
    'encode': ['infile', 'messagefile', 'alpha'],
    'decode': ['infile', 'outfile', 'alpha'],
    'capacity': ['infile', 'outfile', 'alpha'],
    'test': []
    }

parser.add_argument('behavior', type=str, help='interaction modes: {0}'.format(valid_opt_behaviors.keys()))
parser.add_argument('-i', '--infile', type=str, help='path to vessel image (.png)')
parser.add_argument('-o', '--outfile', type=str, help='path to write output file')
parser.add_argument('-m', '--messagefile', type=str, help='path to message file')
parser.add_argument('-a', '--alpha', type=float, help='complexity threshold', default=0.45)
opts = parser.parse_args()

# Fungsi pengecekan file
def check_file_exists(filename):
    if not os.path.exists(filename):
        parser.error('The file "{0}" could not be found.'.format(filename))

if opts.behavior == 'decode':
    check_file_exists(opts.infile)
    decode(opts.infile, opts.outfile, opts.alpha)
elif opts.behavior == 'encode':
    check_file_exists(opts.infile)
    check_file_exists(opts.messagefile)
    encode(opts.infile, opts.messagefile, opts.outfile, opts.alpha)
elif opts.behavior == 'capacity':
    check_file_exists(opts.infile)
    capacity(opts.infile, alpha=opts.alpha, outfile=opts.outfile)
elif opts.behavior == 'test':
    test_all()
