#!/usr/bin/python3


#get_bin = lambda x, n: format(x, 'b').zfill(n)[::-1]
get_bin = lambda x, n: format(x, 'b').zfill(n)

def bytes_to_base2string(bytestr):
    bits = ""
    for c in bytestr:
        bits += get_bin(c, 8)

    return bits

def bytes_to_base2list(bytestr):
    bits = list()
    for c in bytestr:
        bits += [int(v) for v in bin(c)[2:].zfill(8)]

    return bits
        

def file_to_bytes(fname):
    with open(fname, 'rb') as file:
            bytestr = file.read()

    return bytestr

if __name__ == "__main__":
    bs = file_to_bytes("./data/data.sha1")
    bits = bytes_to_base2string(bs)[0:1000]
    print(bits)
