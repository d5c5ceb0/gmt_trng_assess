#!/usr/bin/python3


def berlekamp_massey_algorithm(bits, n):
    b = '1' + '0'*(n-1)
    c = '1' + '0'*(n-1)

    L, m, N = 0, -1, 0
    while (N < n):
        d = int(bits[N],2)
        if L > 0:
            k = int(c[1:L+1], 2)
            h = int(bits[N-L:N][::-1], 2)
            r = bin(k&h)[2:].count('1')
            d = d ^ (r%2)

        if d != 0:
            t = c
            k = int(c[N-m:n], 2)
            h = int(b[0:n-N+m], 2)
            c = c[0:N-m] + bin(k^h)[2:].zfill(n-N+m)
            if L <= (N/2):
                L = N + 1 - L
                m = N
                b = t 
        N = N +1
    return L 

