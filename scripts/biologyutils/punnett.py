#!/usr/bin/python3
import itertools
import collections

def punnett(genepool1 : list, genepool2 : list) -> collections.Counter:
    parentals = [sorted(itertools.product(*genepool1)), sorted(itertools.product(*genepool2))]
    return collections.Counter("".join("".join(i) for i in zip(*j)) for j in itertools.product(*parentals))
