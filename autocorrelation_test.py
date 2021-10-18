#!/usr/bin/python3
# -*- coding=utf-8 -*-

"""
自相关检测

（1）原理：
将序列逻辑左移d位后所得新序列与原序列的关联程度
（2）不通过分析：
序列中0,1变化的过慢
（3）参数设置:
d = 1,2,8
（4）参数要求：
1 <=d <=floor(n/2), (n-d)>10
"""

import math

def autocorrelation_test(bits, d, a):
    """
    autocorrelation test

    args:
        bits: bit stream
        a   : significance level
    rets:
        [n, S, V, a, p_value, p_value >= a]
    """
    n = len(bits)
    m = [int(bits[i])^int(bits[i+d]) for i in range(n-d)]

    S = sum(m)

    V = 2*(S-((n-d)/2))/math.sqrt(n-d)

    p_value = math.erfc(abs(V)/math.sqrt(2))

    return [n, S, V, a, p_value, p_value >= a]

def autocorrelation_logs(n, S, V, a, p_value, result):
    print("\t\t\t       AUTOCORRELATION TEST")
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
    ret = autocorrelation_test(bits, 1, 0.01)
    autocorrelation_logs(*ret)
    ret = autocorrelation_test(bits, 2, 0.01)
    autocorrelation_logs(*ret)
    ret = autocorrelation_test(bits, 8, 0.01)
    autocorrelation_logs(*ret)
    ret = autocorrelation_test(bits, 16, 0.01)
    autocorrelation_logs(*ret)
