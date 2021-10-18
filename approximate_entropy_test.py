#!/usr/bin/python3
# -*- coding=utf-8 -*-

"""
近似熵检测

（1）原理：
比较m位可重叠子序列模式的频数和m+1位可重叠子序列模式的频数
（2）不通过分析：
待检测序列具有较强的规则性
（3）参数设置:
m = 5
（4）参数要求：
m < foor(log2n) - 2
"""

import math
import scipy.special as ss

def approximate_entropy_test(bits, m, a):
    """
    approximate entropy test

    args:
        bits: bit stream
        a   : significance level 
    
    rets:
        [n, ApEn, V, a, p_value, p_value >= a]
    """
    n = len(bits)

    phi = list()
    for mi in range(m, m+2):
        d = bits + bits[0:mi-1]

        vs = [0]*(2**mi)
        for i in range(n):
            vs[int(d[i:i+mi], 2)] += 1
        phi.append(sum([v/n*math.log(v/n) for v in vs if v > 0]))

    ApEn = phi[0] - phi[1]
    V= 2*n*(math.log(2) - ApEn)
    p_value = ss.gammaincc(2**(m-1), V/2)

    return [n, ApEn, V, a, p_value, p_value >= a]

def approximate_entropy_logs(n, ApEn, V, a, p_value, result):
    print("\t\t\t       APPROXIMATE ENTROPY TEST")
    print("\t\t---------------------------------------------")
    print("\t\t COMPUTATIONAL INFORMATION:                  ")
    print("\t\t---------------------------------------------")
    print("\t\t(a) n                   = ", n)
    print("\t\t(b) ApEn                = ", ApEn)
    print("\t\t(c) V                   = ", V)
    print("\t\t(d) a                   = ", a)
    print("\t\t(e) p_value             = ", p_value)
    print("\t\t(f) pass                = ", result)
    print("\t\t---------------------------------------------")
 
if __name__ == '__main__':
    from common import *

    strs = file_to_bytes("./data/data.sha1")
    bits = bytes_to_base2string(strs)
    ret = approximate_entropy_test(bits, 2, 0.01)
    approximate_entropy_logs(*ret)
    ret = approximate_entropy_test(bits, 5, 0.01)
    approximate_entropy_logs(*ret)

