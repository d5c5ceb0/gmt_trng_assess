#!/usr/bin/python3
# -*- coding=utf-8 -*-

"""
重叠子序列检测

（1）原理：
检测待检序列中m位可重叠子序列中每一种模式的个数是否接近（各个模式出现的概率应该均等）。
delta1和delta分别服从自由度为2^(m-1)和2^(m-2)的卡方分布
（2）不通过分析：
序列中长度为m的可重叠子序列模式分布不均匀。
（3）参数设置：
m = 2, 5
（4）参数要求：
m < floor(log_{2}^n)-2
"""

import math
import scipy.special as ss

def serial_test(bits, m, a):
    """
    serial test

    args:
        bits: bit stream
        m   : length of subsequences
        a   : significance level

    rets:
        [n, m, delta1, delta2, a, p_value1, p_value2, (p_value1>a)and(p_value2>a)]
    """

    n = len(bits)
    
    # 由待检序列构造一个新的序列
    d = bits + bits[0:m-1]

    #计算新序列中每一种m位序列模式(共有2^m个)出现的频数
    psis = list()
    for i in range(m, m-3, -1):
        if i <= 0:
            psis.append(0.0)
        else:
            vs = [0]*(2**i)
            for j in range(n):
                vs[int(d[j:j+i], 2)] += 1
            psi = sum([v**2 for v in vs])
            psis.append(2**i/n * psi - n)

    # 计算delta值
    delta1 = psis[0] - psis[1]
    delta2 = psis[0] - 2 * psis[1] + psis[2]

    # 计算P-value1, P-value2
    p_value1 = ss.gammaincc(2**(m-2), delta1/2)
    p_value2 = ss.gammaincc(2**(m-3), delta2/2)

    return [n, m, delta1, delta2, a, p_value1, p_value2, (p_value1>a)and(p_value2>a)]


def serial_logs(n, m, delta1, delta2, a, p_value1, p_value2, result):
    print("\t\t\t       SERIAL TEST")
    print("\t\t---------------------------------------------")
    print("\t\t COMPUTATIONAL INFORMATION:                  ")
    print("\t\t---------------------------------------------")
    print("\t\t(a) n                   = ", n)
    print("\t\t(b) m                   = ", m)
    print("\t\t(c) delta1              = ", delta1)
    print("\t\t(d) delta2              = ", delta2)
    print("\t\t(e) a                   = ", a)
    print("\t\t(f) p_value0            = ", p_value1)
    print("\t\t(g) p_value1            = ", p_value2)
    print("\t\t(h) pass                = ", result)
    print("\t\t---------------------------------------------")


if __name__ == '__main__':
    from common import *

    strs = file_to_bytes("./data/data.sha1")
    bits = bytes_to_base2string(strs)
    ret = serial_test(bits, 2, 0.01)
    serial_logs(*ret)
    ret = serial_test(bits, 5, 0.01)
    serial_logs(*ret)
