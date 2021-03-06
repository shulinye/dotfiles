#!/usr/bin/env python3

from itertools import tee

def verilog_to_latex_timetable(filename, scale=None):
    mapping = {'x':'U','1':'H','0':'L'}
    f = list(zip(*[i.strip().split() for i in open(filename).readlines()[:-1]]))
    times = list(map(int,f[0]))
    scale = max(times[-1]//70,1) if scale is None else scale
    diffs = [i/scale for i in gen_diffs(times)]
    print("Scale=%s" % scale)
    vals = f[1:]
    for line in vals:
        n = line[0].split('=')[0]
        print(n,"&",end=' ',sep=' ')
        v = [mapping[i.split('=')[1]] for i in line]
        print(" ".join(group(diffs, v)), end='')
        print(r"\\")

def group(diffs, vals):
    t = zip(diffs,vals)
    gathered, lastval = next(t)
    for i,j in t:
        if j != lastval:
            yield str(gathered) + lastval
            gathered = i
            lastval = j
        else:
            gathered += i
    yield str(gathered) + lastval

def gen_diffs(li):
    g = iter(li)
    paired = tee(g,2)
    next(paired[1])
    return ((j-i) for i,j in zip(*paired))

if __name__ == "__main__":
    import argparse
