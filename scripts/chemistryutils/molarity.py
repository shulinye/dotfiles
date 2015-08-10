#!/usr/bin/python3
"""Calculations regarding molarity"""
import sys
from os import path

if __name__ == "__main__" and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.realpath(__file__))))

from enum import Enum
import re
from pythonutils import autorepr

BASEPATH = path.dirname(path.realpath(__file__))
ELEMENT_FILE = path.join(BASEPATH, "elements.txt")
MOLECULAR_WEIGHT_FILE = path.join(BASEPATH, "molecular_weights.txt")

class Conversions(Enum):
    re_format = re.compile(r'(\d+)\s*([a-z]+)')
    k = 10**3
    m = 10**(-3)
    u = 10**(-6)
    micro = 10**(-6)

@autorepr
class Element(object):
    def __init__(self, mass, name, symbol, number):
        self.mass = mass
        self.name = name
        self.symbol = symbol
        self.number = number
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        if not isinstance(other, Element): return False
        return self.number == other.number
    def __lt__(self, other):
        return self.number < other.number

elements = {}
with open(ELEMENT_FILE) as f:
    for i in f:
        mass, name, symbol, number = i.split()
        mass = float(mass)
        number = int(number)
        elements[symbol] = Element(mass, name, symbol, number)

chemicals = {}
with open(MOLECULAR_WEIGHT_FILE) as f:
    for i in f:
        k,v = i.split(" = ")
        chemicals[k] = float(v)

def fluid_needed(molarity : float, mw : float , mass : float) -> float:
    """How much liquid do you need for a solution of a specific molarity?"""
    return mass/mw/molarity
