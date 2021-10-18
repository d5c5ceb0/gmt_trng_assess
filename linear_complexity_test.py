#!/usr/bin/python3
# -*- coding=utf-8 -*-

"""
单比特频数检测

（1）原理：
检测各等长子序列的线性复杂度分布是否服从随机性要求
（2）不通过分析：
子序列线性复杂度分布不规则
（3）参数设置:
m = 500
（4）参数要求：
n>=10^6
M属于[500,5000]
N=n//M >=200
"""

import math
import scipy.special as ss
from berlekamp_massey import *

pi = [0.010417,0.03125,0.125,0.5,0.25,0.0625,0.020833]

def linear_complexity_test(bits, m, a):
    """
    linear complexity test

    args:
        bits: bit stream
        m   : length of subsequences
        a   : significance level 
    rets:
        [n, m, N, V, mu, a, p_value, (p_value >= a)]
    """

    n = len(bits)
    N = n//m

    L = list()
    for i in range(N):
        L.append(berlekamp_massey_algorithm(bits[i*m:(i+1)*m], m))

    mu = m/2 + (9+(-1)**(m+1))/36 - (m/3+2/9)/(2**m)

    T = list()
    for i in range(N):
        T.append((-1)**m * (L[i]-mu) + 2/9)
    
    v = [0]*7
    for t in T:
        if t <= -2.5:
            v[0] += 1
        elif t <= -1.5:
            v[1] += 1
        elif t <= -0.5:
            v[2] += 1
        elif t <= 0.5:
            v[3] += 1
        elif t <= 1.5:
            v[4] += 1
        elif t <= 2.5:
            v[5] += 1
        else:
            v[6] += 1

    V = 0
    for i in range(7):
        V += (v[i] - N*pi[i])**2/(N*pi[i])

    p_value =  ss.gammaincc(3, V/2)

    return [n, m, N, V, mu, a, p_value, (p_value >= a)]

def linear_complexity_logs(n, m, N, V, mu, a, p_value, result):
    print("\t\t\t       LINEAR COMPLEXITY TEST")
    print("\t\t---------------------------------------------")
    print("\t\t COMPUTATIONAL INFORMATION:                  ")
    print("\t\t---------------------------------------------")
    print("\t\t(a) n                   = ", n)
    print("\t\t(b) m                   = ", m)
    print("\t\t(c) N                   = ", N)
    print("\t\t(d) V                   = ", V)
    print("\t\t(e) mu                  = ", mu)
    print("\t\t(f) a                   = ", a)
    print("\t\t(g) p_value             = ", p_value)
    print("\t\t(h) pass                = ", result)
    print("\t\t---------------------------------------------")

if __name__ == '__main__':
    from common import *

    strs = file_to_bytes("./data/data.sha1")
    bits = bytes_to_base2string(strs)
    ret = linear_complexity_test(bits, 500, 0.01)
    linear_complexity_logs(*ret)
