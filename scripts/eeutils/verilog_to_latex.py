#!/usr/bin/env python3

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.realpath(__file__))))

from pythonutils import gen_diffs

def verilog_to_latex_timetable(filename, scale=None):
    mapping = {'x':'U','1':'H','0':'L'}
    lines = open(filename).readlines()
    f = list(zip(*[i.strip().split() for i in lines[:-1]]))
    times = list(map(int,f[0])) + [int(lines[-1].split()[-1])]
    scale = max(times[-1]//60,1) if scale is None else scale
    diffs = [i/scale for i in gen_diffs(times)]
    yield 'Scale=%s' % scale
    vals = f[1:]
    for line in vals:
        if '|' in line[0]:
            yield r'\\'
            continue
        n = line[0].split('=')[0]
        v = [mapping[i.split('=')[1]] for i in line]
        yield r'%s & %s \\' % (n, ' '.join(group(diffs,v)))

def group(diffs, vals):
    t = zip(diffs,vals)
    gathered, lastval = next(t)
    for i,j in t:
        if j != lastval:
            yield '%.2f'% gathered + lastval
            gathered = i
            lastval = j
        else:
            gathered += i
    yield '%.2f' % gathered + lastval

if __name__ == '__main__':
    import argparse
