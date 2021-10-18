#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
扑克检测

(1) 原理：
长度为m的子序列有2^m种。以此长度划分带检测序列，检测子序列的个数是否接近。统计值V
应该服从自由度为(2^m-1)的卡方(x^2)分布
(2) 不通过分析：
有某个或者某几个子序列的个数过多或者过少。
(3) 参数设置：
m = 4,8
(4) 参数要求：
floor(n/m) >= 5 * 2^m
"""

import math
import scipy.special as ss


def poker_test(bits, m, a):
    """
    poker test

    args:
        bits: bit stream
        m   : length of subsequences
        a   : significance level

    rets:
        [n, m, N, V, a, p_value, p_value>=a]
    """

    n = len(bits)

    # 将带检测序列分为N个长度为m的非重叠子序列
    N = n//m

    # 统计第i种子序列模式出现的频数
    ni = [0]*(2**m)
    for i in range(N):
        ni[int(bits[i*m : (i+1)*m], 2)] += 1

    # 计算统计值V
    V = 0
    for v in ni:
        V += v**2
    V = (2**m / N)*V - N

    # 计算P-value
    p_value = ss.gammaincc((2**m - 1)/2, V/2)

    return [n, m, N, V, a, p_value, p_value>=a]

def poker_logs(n, m, N, V, a, p_value, result):
    print("\t\t\t       POKER TEST")
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
    ret = poker_test(bits, 4, 0.01)
    poker_logs(*ret)
    ret = poker_test(bits, 8, 0.01)
    poker_logs(*ret)
