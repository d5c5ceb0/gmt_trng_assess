#!/usr/bin/python3

import sys
import json
import progressbar
from common import *
from monobit_frequency_test import monobit_frequency_test
from frequency_test_within_a_block_test import frequency_test_within_a_block_test
from poker_test import poker_test
from serial_test import serial_test
from runs_test import runs_test
from runs_distribution_test import runs_distribution_test
from longest_run_of_ones_in_a_block_test import longest_run_of_ones_in_a_block_test
from binary_derivative_test import binary_derivative_test
from autocorrelation_test import autocorrelation_test
from binary_matrix_rank_test import binary_matrix_rank_test
from cumulative_sums_test import cumulative_sums_test
from approximate_entropy_test import approximate_entropy_test
from linear_complexity_test import linear_complexity_test
from maurer_universal_statistical_test import maurer_universal_statistical_test
from discrete_fourier_transform_test import discrete_fourier_transform_test



conf_name = "./config.json"

test_vectors = {
    "monobit_frequency_test"              : (monobit_frequency_test,              True),
    "frequency_test_within_a_block_test"  : (frequency_test_within_a_block_test,  True),
    "poker_test"                          : (poker_test,                          True),
    "serial_test"                         : (serial_test,                         True),
    "runs_test"                           : (runs_test,                           True),
    "runs_distribution_test"              : (runs_distribution_test,              True),
    "longest_run_of_ones_in_a_block_test" : (longest_run_of_ones_in_a_block_test, True),
    "binary_derivative_test"              : (binary_derivative_test,              True),
    "autocorrelation_test"                : (autocorrelation_test,                True),
    "binary_matrix_rank_test"             : (binary_matrix_rank_test,             True),
    "cumulative_sums_test"                : (cumulative_sums_test,                True),
    "approximate_entropy_test"            : (approximate_entropy_test,            True),
    "linear_complexity_test"              : (linear_complexity_test,              True),
    "maurer_universal_statistical_test"   : (maurer_universal_statistical_test,   True),
    "discrete_fourier_transform_test"     : (discrete_fourier_transform_test,     True),
}

test_results = {
    "monobit_frequency_test"                     : [],
    "frequency_test_within_a_block_test"         : [],
    "poker_test"                                 : [],
    "serial_test"                                : [],
    "runs_test"                                  : [],
    "runs_distribution_test"                     : [],
    "longest_run_of_ones_in_a_block_test"        : [],
    "binary_derivative_test"                     : [],
    "autocorrelation_test"                       : [],
    "binary_matrix_rank_test"                    : [],
    "cumulative_sums_test"                       : [],
    "approximate_entropy_test"                   : [],
    "linear_complexity_test"                     : [],
    "maurer_universal_statistical_test"          : [],
    "discrete_fourier_transform_test"            : [],
}


def init_result(config):
    for k,v in test_vectors.items():
        test_results[k] = [0]*len(config[k])

def main():
    with open(conf_name, 'r') as file:
        config = json.load(file)

    num_of_bits_per_stream = config['num_of_bits_per_stream']
    num_of_streams = config['num_of_streams']
    threshold = config['threshold']

    if len(sys.argv) != 5 and len(sys.argv) != 2:
        print("args error")
        sys.exit()

    fname = sys.argv[1]
    if len(sys.argv) == 5:
        num_of_bits_per_stream = int(sys.argv[2])
        num_of_streams = int(sys.argv[3])
        threshold = int(sys.argv[4])

    init_result(config)

    with open(fname, 'rb') as file:
        for i in progressbar.progressbar(range(num_of_streams)):
            if num_of_bits_per_stream%8 != 0:
                print("no align size")
                sys.exit()
            strs = file.read(num_of_bits_per_stream//8)
            bits = bytes_to_base2string(strs)
            din = bits[0:num_of_bits_per_stream]

            for k,v in test_vectors.items():
                args = config[k]
                for j in range(len(args)):
                    arg = args[j]
                    if v[1] == True:
                        ret = v[0](din, *list(arg.values()))
                        if ret[-1] == True:
                            test_results[k][j] += 1

    print("\nassess report(total {} rounds): ".format(num_of_streams))
    print("{:38}{:18}{:10}".format("<TEST>","<PROPORTION>","<PASS>"))
    print("-"*(38+18+10))
    for k, v in test_results.items():
        print("{:38}{:18}{:10}".format(k, ",".join('%s' %a for a in
            v),",".join('%s' %a for a in [p > threshold for p in v])))
    print("-"*(38+18+10))


if __name__ == '__main__':
    main()

