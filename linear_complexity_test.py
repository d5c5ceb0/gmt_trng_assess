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
import time

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

    L = [berlekamp_massey_algorithm(bits[i*m:(i+1)*m], m) for i in range(N)]
    mu = m/2 + (9+(-1)**(m+1))/36 - (m/3+2/9)/(2**m)
    T = [(-1)**m * (L[i]-mu) + 2/9 for i in range(N)]
    
    v = [0]*7
    v[0] = len([v for v in T if v <= -2.5])
    v[1] = len([v for v in T if v <= -1.5 and v > -2.5])
    v[2] = len([v for v in T if v <= -0.5 and v > -1.5])
    v[3] = len([v for v in T if v <= 0.5 and v > -0.5])
    v[4] = len([v for v in T if v <= 1.5 and v > 0.5])
    v[5] = len([v for v in T if v <= 2.5 and v > 1.5])
    v[6] = len([v for v in T if v > 2.5  ])

    V = sum((v[i] - N*pi[i])**2/(N*pi[i]) for i in range(7))

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
    print(time.time())
    ret = linear_complexity_test(bits, 500, 0.01)
    print(time.time())
    linear_complexity_logs(*ret)
