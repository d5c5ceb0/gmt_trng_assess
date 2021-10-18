#!/usr/bin/python3
# -*- coding=utf-8 -*-

"""
矩阵秩检测

（1）原理：
由待检测序列的给定长度子序列构造矩阵，检测所构造矩阵行或者列之间的线性独立性
（2）不通过分析：
秩分布差别比较大
（3）参数设置:
M=Q=32
（4）参数要求：
M=32,Q=32,n>=M*Q,n-N*M*Q要小
"""

import scipy.special as sc
from matrix import *

def binary_matrix_rank_test(bits, M, Q, a):
    """
    binary matrix rank test

    args:
        bits: bit stream
        M   : number of rows in each matrix
        Q   : number of columns in each matrix
        a   : significance level 

    rets:
        [n, N, FM, FM1, V, a, p_value, (p_value >= a)]
    """

    n = len(bits)
    MQ = M * Q
    N = n//MQ
    
    FM = 0
    FM1 = 0
    F = 0
    for i in range(N):
        blist = list(bits[i*MQ : (i+1)*MQ])
        barr = create_matrix(M, Q, [int(v) for v in blist])
        R = computeRank(M, Q, barr)
        if R == M:
            FM += 1
        elif R == (M-1):
            FM1 += 1
        else:
            F += 1


    V = (FM-0.2888*N)**2/(0.2888*N) + (FM1-0.5776*N)**2/(0.5776*N) + (F-0.1336*N)**2/(0.1336*N)

    p_value = sc.gammaincc(1, V/2)

    return [n, N, FM, FM1, V, a, p_value, (p_value >= a)]

def binary_matrix_rank_logs(n, N, FM, FM1, V, a, p_value, result):
    print("\t\t\t       BINARY MATRIX RANK TEST")
    print("\t\t---------------------------------------------")
    print("\t\t COMPUTATIONAL INFORMATION:                  ")
    print("\t\t---------------------------------------------")
    print("\t\t(a) n                   = ", n)
    print("\t\t(b) N                   = ", N)
    print("\t\t(c) FM                  = ", FM)
    print("\t\t(e) FM1                 = ", FM1)
    print("\t\t(e) V                   = ", V)
    print("\t\t(f) a                   = ", a)
    print("\t\t(g) p_value             = ", p_value)
    print("\t\t(h) pass                = ", result)
    print("\t\t---------------------------------------------")

if __name__ == '__main__':
    from common import *

    strs = file_to_bytes("./data/data.sha1")
    bits = bytes_to_base2string(strs)
    ret = binary_matrix_rank_test(bits, 32, 32, 0.01)
    binary_matrix_rank_logs(*ret)
