#!/usr/bin/env python3

from itertools import tee

__all__= ['gen_diffs']

def gen_diffs(li):
    """Takes the diff between neighboring values in a stream"""
    paired = tee(li,2)
    next(paired[1])
    return ((j-i) for i,j in zip(*paired))
