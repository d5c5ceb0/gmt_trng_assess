#!/usr/bin/python3
# -*- coding=utf-8 -*-

"""
离散傅立叶检测

（1）原理：
使用频谱方法检测待检测序列进行傅立叶变换后的尖峰高度是否超过某个门限值
（2）不通过分析：
太多傅立叶变换的尖峰高度超过门限值
（3）参数设置:
无
（4）参数要求：
n > 1000
"""

import math
import numpy as np

def discrete_fourier_transform_test(bits, a):
    """
    Discrete Fourier Transform Test

    args:
        bits: bit stream
        a   : significance level 
    rets:
        [n, T, N0, N1, V, a, p_value, p_value >= a]
    """
    n = len(bits)

    l = [2*int(v)-1 for v in list(bits)]

    fl = np.fft.fft(np.array(l))

    fla = abs(fl)[0:(n//2)]

    T = math.sqrt(2.995732274*n)

    N0 =  0.95 * n / 2

    N1 = len([v for v in fla if v < T])

    V = (N1 - N0)/math.sqrt((n*0.95*0.05)/4)

    p_value = math.erfc(abs(V)/math.sqrt(2))

    return [n, T, N0, N1, V, a, p_value, p_value >= a]

def discrete_fourier_transform_log(n, T, N0, N1, V, a, p_value, result):
    print("\t\t\t       DISCRETE FOURIER TRANSFORM TEST")
    print("\t\t---------------------------------------------")
    print("\t\t COMPUTATIONAL INFORMATION:                  ")
    print("\t\t---------------------------------------------")
    print("\t\t(a) n                   = ", n)
    print("\t\t(b) S                   = ", T)
    print("\t\t(c) N0                  = ", N0)
    print("\t\t(d) N1                  = ", N1)
    print("\t\t(e) V                   = ", V)
    print("\t\t(f) a                   = ", a)
    print("\t\t(g) p_value             = ", p_value)
    print("\t\t(h) pass                = ", result)
    print("\t\t---------------------------------------------")
 
if __name__ == '__main__':
    from common import *

    strs = file_to_bytes("./data/data.sha1")
    bits = bytes_to_base2string(strs)
    ret = discrete_fourier_transform_test(bits, 0.01)
    discrete_fourier_transform_log(*ret)
