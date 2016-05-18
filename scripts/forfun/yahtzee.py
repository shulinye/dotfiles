#!/usr/bin/env python3

import enum
import random

dice = enum.Enum('dice', "⚀ ⚁ ⚂ ⚃ ⚄ ⚅")

def roll():
    return [random.randint(1,6) for _ in range(5)]

def reroll(original, indices):
    return [random.randint(1,6) if i in indices else orig for orig,i in zip(original,range(5))]
