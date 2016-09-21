#!/usr/bin/env python3

def parallel_resistors(*resistors):
    import fractions
    return 1/sum(fractions.Fraction(1,r) for r in resistors)



