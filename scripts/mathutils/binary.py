#!/usr/bin/env python3

def decimal_to_binary(n, prefix = "0b"):
    output = []
    while n > 0:
        n,r = divmod(n,2)
        output.append(r)
    return prefix + "".join(map(str, output[::-1]))

def decimal_to_BCD(n):
    s = str(n)
    return " ".join(decimal_to_binary(int(i), prefix='').zfill(4) for i in s)
