#!/usr/bin/python3
import itertools
import collections

def punnettParse(s : str) -> list:
    """Take a str and turn it into a list of strings punnett can accept"""
    if len(s) % 2: raise ValueError('Even number of alleles required')
    return ["".join(sorted(s[i:i+2])) for i in range(0,len(s),2)]

def punnett(genepool1 : list, genepool2 : list) -> collections.Counter:
    if len(genepool1) != len(genepool2):
        raise ValueError("Genepools must be same length")
    parentals = [sorted(itertools.product(*genepool1)), sorted(itertools.product(*genepool2))]
    genes = (zip(*j) for j in itertools.product(*parentals))
    c = collections.Counter("".join("".join(sorted(j, reverse=True)) for j in i) for i in genes)
    normalize = sum(c.values())
    for i in c: c[i] /= normalize
    return c

def inbreed_f1(counter):
    c = counter.items()
    output = collections.Counter()
    for i, j in itertools.product(c,c):
        offspring = punnett(*map(punnettParse, [i[0], j[0]]))
        for kid in offspring: offspring[kid] *= i[1]*j[1]
        output += offspring
    return output

def recessive_f1(counter, recessive = None):
    if recessive is None:
        recessive = c.keys()[0].lower()
    output = collections.Counter()
    c = counter.items()
    normalize = sum(counter.values())
    for i in c:
        offspring = punnett(*map(punnettParse, [i[0], recessive]))
        for kid in offspring: offspring[kid] *= i[1]
        output += offspring
    return output

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('genepools', nargs=2, help="Genes. Like AaBb")
    args = parser.parse_args()
    print(punnett(*map(punnettParse, args.genepools)))
