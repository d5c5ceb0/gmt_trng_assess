#!/usr/bin/python3
# -*- coding=utf-8 -*-


import math
import scipy.special as ss

"""
块内最大1游程检测

（1）原理：
N个等长子序列，检测各个子序列中最大1的游程的分布是否规则
（2）不通过分析：
待检测序列中有很多成簇的1或者0
（3）参数设置：
m = 10000
（4）参数要求：
当M=8时，N>=16, n = N*M
"""


MPI8     = [(1, 0.2148), (2, 0.3672), (3, 0.2305), (4, 0.1875)]
MPI128   = [(4, 0.1174), (5, 0.2430), (6, 0.2493), (7, 0.1752), (8, 0.1027), (9, 0.1124)]
MPI10000 = [(10, 0.0882), (11, 0.2092), (12, 0.2483), (13, 0.1933), (14, 0.1208), (15, 0.0675), (16, 0.0727)]
MPIs = {8:MPI8, 128:MPI128, 10000:MPI10000}
Ks = {8:3, 128:5, 10000:6}

def longest_run_of_ones_in_a_block_test(bits, m, a):
    """
    frequency test within a block

    args:
        bits: bit stream
        m   : block size
        a   : significance level

    rets:
        [n, m, N, V, a, p_value, p_value >= a]
    """

    n = len(bits)
    MPI = MPIs[m]
    K = Ks[m]

    # 将待检测序列分为N个长度为m的非重叠子序列
    N = n//m

    # 计算每个子序列中最大游程的长度
    vs = [0] * (K+1)
    for i in range(N):
        maxlen = 0
        current = 0
        for b in bits[i*m : (i+1)*m]:
            if b == '1':
                current += 1
                if (current> maxlen):
                    maxlen = current
            else:
                current = 0

        if maxlen < MPI[0][0]:
            vs[0] += 1
        elif maxlen > MPI[-1][0]:
            vs[-1] += 1
        else:
            vs[maxlen-MPI[0][0]] += 1


    # 计算统计值V
    V = sum([((vs[i] - N*MPI[i][1])**2/(N * MPI[i][1])) for i in range(len(MPI))])

    # 计算P-value
    p_value = ss.gammaincc(K/2, V/2)

    return [n, m, N, V, a, p_value, p_value >= a]

def longest_run_of_ones_in_a_block_logs(n, m, N, V, a, p_value, result):
    print("\t\t\t       LONGEST RUNS TEST")
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
    ret = longest_run_of_ones_in_a_block_test(bits, 10000, 0.01)
    longest_run_of_ones_in_a_block_logs(*ret)
