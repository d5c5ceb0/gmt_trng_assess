#!/usr/bin/python3
# -*- coding=utf-8 -*-

import math
import scipy.special as ss

"""
游程分布检测

（1）原理：
检测相同长度游程的数目是否接近一致。
（2）不通过分析：
相同长度的游程数目分配不均匀。
（3）参数配置：
无
（4）参数要求：
n >= 100
"""

def runs_distribution_test(bits, a):
    """
    runs distribution test

    args:
        bits: bit stream
        a   : significance level

    rets:
        [n, V, a, p_value, (p_value >= a)]
    """

    n = len(bits)

    # 计算ei
    for i in range(1, n+1):
        if (n - i + 3)/(pow(2,(i+2))) < 5:
            break
        k = i
    ei = [(n - i + 3)/(2**(i+2)) for i in range(1,k+1)]

    # 统计待检测序列中每个游程的长度
    current = 0
    bi = [0]*k
    gi = [0]*k
    for b in bits:
        if b == '1':
            if current <= 0:
                if abs(current) <= k and abs(current) >= 1:
                    gi[abs(current)-1] += 1;
                current = 1
            else:
                current += 1
        else:
            if current >= 0:
                if abs(current) <= k and abs(current) >= 1:
                    bi[abs(current)-1] += 1;
                current = -1
            else:
                current -= 1

    # 计算V
    V = 0
    for i in range(k):
        V += ((bi[i]-ei[i])**2 + (gi[i]-ei[i])**2)/ei[i]

    # 计算P-value
    p_value = ss.gammaincc(k-1, V/2)

    return [n, V, a, p_value, (p_value >= a)]

def runs_distribution_logs(n, V, a, p_value, result):
    print("\t\t\t       RUNS DISTRIBUTION TEST")
    print("\t\t---------------------------------------------")
    print("\t\t COMPUTATIONAL INFORMATION:                  ")
    print("\t\t---------------------------------------------")
    print("\t\t(a) n                   = ", n)
    print("\t\t(b) V                   = ", V)
    print("\t\t(c) a                   = ", a)
    print("\t\t(d) p_value             = ", p_value)
    print("\t\t(e) pass                = ", result)
    print("\t\t---------------------------------------------")

if __name__ == '__main__':
    from common import *

    strs = file_to_bytes("./data/data.sha1")
    bits = bytes_to_base2string(strs)
    ret = runs_distribution_test(bits, 0.01)
    runs_distribution_logs(*ret)
