#!/usr/bin/python3
import argparse
import itertools
import collections

def punnettParse(s : str) -> list:
    if len(s) % 2: raise ValueError('Even number of alleles required')
    return [s[i] + s[i+1] for i in range(0,len(s),2)]

def punnett(genepool1 : list, genepool2 : list) -> collections.Counter:
    if len(genepool1) != len(genepool2): raise ValueError("Genepools must be same length")
    parentals = [sorted(itertools.product(*genepool1)), sorted(itertools.product(*genepool2))]
    return collections.Counter("".join("".join(i) for i in zip(*j)) for j in itertools.product(*parentals))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('genepools', nargs=2, help="Genes. Like AaBb")
    args = parser.parse_args()
    print(punnett(*map(punnettParse, args.genepools)))
