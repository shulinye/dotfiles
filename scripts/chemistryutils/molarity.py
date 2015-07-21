#!/usr/bin/python3

from enum import Enum

class Conversions(Enum):
    m = 10**(-3)
    u = 10**(-6)

class Chemicals(Enum):
    silver_nitrate = 169.87
    ascorbic_acid = 176.12
    sodium_borohydride = 37.83

def fluid_needed(molarity, mw, mass):
    return mass/mw/molarity
