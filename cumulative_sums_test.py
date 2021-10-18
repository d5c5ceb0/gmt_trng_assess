#!/usr/bin/python3
# -*- coding=utf-8 -*-

"""
累加和检测

（1）原理：
最大累加和与随即序列应具有的最大偏移相比较，应该接近于0
（2）不通过分析：
说明待检测序列头部有过多的0或者1
（3）参数设置:
无
（4）参数要求：
n > 100
"""

import math
from scipy.stats import norm

def cumulative_sums_test(bits, a):
    """
    cumulative sums test

    args:
        bits: bit stream
        a   : significance level 
    rets:
        [n, Z, sum1, sum2, a, p_value, p_value >= a]
    """

    n = len(bits)
    d = [2*int(v)-1 for v in bits]

    S = d[0:1]
    for i in range(1,n):
        S.append(S[-1]+d[i])
    Z = max([abs(v) for v in S])

    sum1 = 0
    for i in range(int((-n/Z+1)/4), int((n/Z-1)/4)+1):
        phi1 = norm.cdf(((4*i+1)*Z)/math.sqrt(n))
        phi2 = norm.cdf(((4*i-1)*Z)/math.sqrt(n))
        sum1 += phi1 - phi2

    sum2 = 0
    for i in range(int((-n/Z-3)/4), int((n/Z-1)/4)+1):
        phi1 = norm.cdf(((4*i+3)*Z)/math.sqrt(n))
        phi2 = norm.cdf(((4*i+1)*Z)/math.sqrt(n))
        sum2 += phi1 - phi2

    p_value = 1 - sum1 + sum2

    return [n, Z, sum1, sum2, a, p_value, p_value >= a]

def cumulative_sums_logs(n, Z, sum1, sum2, a, p_value, result):
    print("\t\t\t       CUMULATIVE SUMS TEST")
    print("\t\t---------------------------------------------")
    print("\t\t COMPUTATIONAL INFORMATION:                  ")
    print("\t\t---------------------------------------------")
    print("\t\t(a) n                   = ", n)
    print("\t\t(b) Z                   = ", Z)
    print("\t\t(c) sum1                = ", sum1)
    print("\t\t(d) sum2                = ", sum2)
    print("\t\t(e) a                   = ", a)
    print("\t\t(f) p_value             = ", p_value)
    print("\t\t(g) pass                = ", result)
    print("\t\t---------------------------------------------")

 
if __name__ == '__main__':
    from common import *

    strs = file_to_bytes("./data/data.sha1")
    bits = bytes_to_base2string(strs)
    ret = cumulative_sums_test(bits, 0.01)
    cumulative_sums_logs(*ret)
