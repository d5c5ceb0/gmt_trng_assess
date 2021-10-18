#!/usr/bin/python3
# -*- coding=utf-8 -*-

"""
单比特频数检测

（1）原理：
检测待检测序列中的0和1的个数是否接近。其统计值V应该服从标准正态分布。
（2）不通过分析：
说明0或者1个数过小。
（3）参数设置:
无
（4）参数要求：
n > 100
"""

import math

def monobit_frequency_test(bits, a):
    """
    monobit frequency test

    args:
        bits: bit stream
        a   : significance level

    rets:
        [n, S, V, a, p_value, p_value>=a]
    """
    
    n = len(bits)

    # 将带检测序列中的0和1分别转换成-1和1
    X = [(2*int(v) - 1) for v in bits]

    # 对其累加求和得S
    S = sum(X)

    # 计算统计值
    V = abs(S)/math.sqrt(n)

    # 计算P-value
    p_value = math.erfc(V/math.sqrt(2))

    return [n, S, V, a, p_value, p_value>=a]

def monobit_frequency_logs(n, S, V, a, p_value, result):
    print("\t\t\t       MONOBIT FREQUENCY TEST")
    print("\t\t---------------------------------------------")
    print("\t\t COMPUTATIONAL INFORMATION:                  ")
    print("\t\t---------------------------------------------")
    print("\t\t(a) n                   = ", n)
    print("\t\t(b) S                   = ", S)
    print("\t\t(c) V                   = ", V)
    print("\t\t(d) a                   = ", a)
    print("\t\t(e) p_value             = ", p_value)
    print("\t\t(f) pass                = ", result)
    print("\t\t---------------------------------------------")
 
if __name__ == '__main__':
    from common import *

    strs = file_to_bytes("./data/data.sha1")
    bits = bytes_to_base2string(strs)
    ret = monobit_frequency_test(bits, 0.01)
    monobit_frequency_logs(*ret)
