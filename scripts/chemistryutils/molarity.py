#!/usr/bin/python3

"""Calculations regarding molarity"""

from enum import Enum
import re

class Conversions(Enum):
    re_format = re.compile(r'(\d+)\s*([a-z]+)')
    k = 10**3
    m = 10**(-3)
    u = 10**(-6)
    micro = 10**(-6)

chemicals = {}
with open("molecular_weights.txt") as f:
    for i in f:
        k,v = i.split(" = ")
        chemicals[k] = float(v)

def fluid_needed(molarity : float, mw : float , mass : float) -> float:
    """How much liquid do you need for a solution of a specific molarity?"""
    return mass/mw/molarity
