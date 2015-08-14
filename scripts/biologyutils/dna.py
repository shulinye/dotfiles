#!/usr/bin/python3

__all__ = ['dna_to_rna']

import sys
if sys.version_info.major <= 2:
    from string import maketrans
    dna_rna_tbl = maketrans('ATGC', 'UACG')
else:
    dna_rna_tbl = dict(zip(map(ord,'ATGC'), 'UACG'))

def dna_to_rna(s):
    return s.translate(dna_rna_tbl)
