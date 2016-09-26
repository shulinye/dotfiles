#!/usr/bin/env python3

from operator import add, and_, or_, xor
import inspect
from itertools import product
from functools import partial, reduce

def truth_table_inputs(n):
    return product(range(2), repeat=n)

def generate_truth_table(func):
    params = inspect.signature(func).parameters
    params = filter(lambda x: params[x].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD, params)
    output = [list(params) + [func.__name__]]
    for i in truth_table_inputs(len(params)):
        output.append(list(i) + [func(*i)])
    return output

def or_gate(*args):
    return any(args)

def nor_gate(*args):
    return not(or_gate(*args))

def and_gate(*args):
    return all(args)

def nand_gate(*args):
    return not(and_gate(*args))


