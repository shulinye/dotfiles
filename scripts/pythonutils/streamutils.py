#!/usr/bin/env python3

from itertools import tee

__all__= ['gen_diffs']

def gen_diffs(li):
    g = iter(li)
    paired = tee(g,2)
    next(paired[1])
    return ((j-i) for i,j in zip(*paired))
