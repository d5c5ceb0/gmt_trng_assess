#!/usr/bin/python3
# -*- coding=utf-8 -*-

"""
游程总数检测

（1）原理：
检测游程总数服从随机性要求。
（2）不通过分析
说明序列中元素变化过快或者过慢。
（3）参数配置：
无
（4）参数要求：
n >= 100
"""

import math


def runs_test(bits, a):
    """
    runs_test

    args:
        bits: bit stream
        a   : significance level 
    
    rets:
        [vobs, pi, a, p_value, p_value >= a]
    """
    
    n = len(bits)

    # 对长度为n的待检序列计算Vobs
    vobs = sum([ 1 if bits[i] != bits[i+1] else 0 for i in range(n-1)]) + 1

    # 计算序列中1的比例
    pi = bits.count('1')/n

    # 计算P-value
    p_value = math.erfc(abs(vobs-2*n*pi*(1-pi))/(2*math.sqrt(2*n)*pi*(1-pi)))

    return [n, vobs, pi, a, p_value, p_value >= a]


def runs_logs(n, vobs, pi, a, p_value, result):
    print("\t\t\t       RUNS TEST")
    print("\t\t---------------------------------------------")
    print("\t\t COMPUTATIONAL INFORMATION:                  ")
    print("\t\t---------------------------------------------")
    print("\t\t(a) n                   = ", n)
    print("\t\t(b) vobs                = ", vobs)
    print("\t\t(c) pi                  = ", pi)
    print("\t\t(d) a                   = ", a)
    print("\t\t(e) p_value             = ", p_value)
    print("\t\t(f) pass                = ", result)
    print("\t\t---------------------------------------------")

if __name__ == '__main__':
    from common import *

    strs = file_to_bytes("./data/data.sha1")
    bits = bytes_to_base2string(strs)
    ret = runs_test(bits, 0.01)
    runs_logs(*ret)

