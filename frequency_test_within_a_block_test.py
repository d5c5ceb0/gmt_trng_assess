#!/usr/bin/python3
# -*- coding=utf-8 -*-

"""
块内频数检测

（1）原理：
m位子序列中1的个数是否接近m/2。统计值V应该服从自由度为N的卡方分布。
（2）不通过分析：
m位子序列中0、1比例不均衡。
（3）参数设置：
m = 100
（4）参数要求：
n>=100, m>=20
"""

import math
import scipy.special as ss


def frequency_test_within_a_block_test(bits, m, a):
    """
    frequency test within a block

    args:
        bits: bit stream
        m   : block size
        a   : significance level

    rets:
        [n, m, N, V, a, p_value, p_value>=a]
    """

    n = len(bits)

    # 将待检测序列分成N个长度为m的非重叠子序列
    N = n//m

    # 计算每个子序列中1所占的比例pi
    pi = [bits[i*m:(i+1)*m].count('1')/m for i in range(N)]

    # 计算统计量V
    V = 4*m*sum([(v - 0.5)**2 for v in pi])

    # 计算P-value
    p_value = ss.gammaincc((N/2),(V/2))

    return [n, m, N, V, a, p_value, p_value>=a]

def frequency_test_within_a_block_logs(n, m, N, V, a, p_value, result):
    print("\t\t\t       FREQUENCY TEST WITHIN A BLOCK")
    print("\t\t---------------------------------------------")
    print("\t\t COMPUTATIONAL INFORMATION:                  ")
    print("\t\t---------------------------------------------")
    print("\t\t(a) n                   = ", n)
    print("\t\t(b) m                   = ", m)
    print("\t\t(c) N                   = ", N)
    print("\t\t(d) V                   = ", V)
    print("\t\t(e) a                   = ", a)
    print("\t\t(f) p_value             = ", p_value)
    print("\t\t(g) pass                = ", result)
    print("\t\t---------------------------------------------")

if __name__ == '__main__':
    from common import *

    strs = file_to_bytes("./data/data.sha1")
    bits = bytes_to_base2string(strs)
    ret = frequency_test_within_a_block_test(bits, 100, 0.01)
    frequency_test_within_a_block_logs(*ret)
