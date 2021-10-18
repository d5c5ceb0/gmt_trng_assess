#!/usr/bin/python3
# -*- coding=utf-8 -*-

"""
通用统计检测

（1）原理：
待检测序列是否可被无损压缩
（2）不通过分析：
待检测序列可大幅度地被无损压缩
（3）参数设置:
无
（4）参数要求：
n=(Q+K)*L, L属于[1,16],Q>=10*2^L, K=floor(n/L)-Q(约等于1000*2^L)
"""

import math

expected = [
    0,         0,         0,         0,
    0,         0,         5.2177052, 6.1962507,
    7.1836656, 8.1764248, 9.1723243, 10.170032,
    11.168765, 12.168070, 13.167693, 14.167488,
    15.167379
]
variance = [
    0,     0,     0,     0,
    0,     0,     2.954, 3.125,
    3.238, 3.311, 3.356, 3.384,
    3.401, 3.410, 3.416, 3.419,
    3.421
]

def maurer_universal_statistical_test(bits, a):
    """
    maurer's universal statistical test

    args:
        bits: bit stream
        a   : significance level
    rets:
        [n, L, Q, K, V, a, p_value, (p_value > a)]
    """

    n = len(bits)
    L = 7
    Q = 1280
    K = n//L - Q

    ilist = bits[0:Q*L]
    tlist = bits[Q*L:(Q+K)*L]

    T = [0]*(2**L)
    for i in range(Q):
        T[int(ilist[i*L:(i+1)*L], 2)] = i+1

    sum = 0
    for i in range(K):
        j = int(tlist[i*L:(i+1)*L],2)
        sum += math.log(Q+i+1-T[j], 2)
        T[j] = Q + i + 1

    sigma = (0.7 -0.8/L + (4 + 32/L)*(K**(-3/L))/15)*math.sqrt(variance[L]/K)
    V = (sum/K - expected[L])/sigma
    p_value = math.erfc(abs(V)/math.sqrt(2))

    return [n, L, Q, K, V, a, p_value, (p_value > a)]


def maurer_universal_statistica_logs(n, L, Q, K, V, a, p_value, result):
    print("\t\t\t       MAURER UNIVERSAL STATISTICA TEST")
    print("\t\t---------------------------------------------")
    print("\t\t COMPUTATIONAL INFORMATION:                  ")
    print("\t\t---------------------------------------------")
    print("\t\t(a) n                   = ", n)
    print("\t\t(b) L                   = ", L)
    print("\t\t(c) Q                   = ", Q)
    print("\t\t(d) K                   = ", K)
    print("\t\t(e) V                   = ", V)
    print("\t\t(f) a                   = ", a)
    print("\t\t(g) p_value             = ", p_value)
    print("\t\t(h) pass                = ", result)
    print("\t\t---------------------------------------------")

if __name__ == '__main__':
    from common import *

    strs = file_to_bytes("./data/data.sha1")
    bits = bytes_to_base2string(strs)
    ret = maurer_universal_statistical_test(bits, 0.01)
    maurer_universal_statistica_logs(*ret)
