#!/usr/bin/python

import sys

__all__ = ['coerced_input']

if sys.version_info.major <= 2:
    input = raw_input

def coerced_input(prompt, _type = float):
    """Continue asking user for input
    until they give one that's of a type
    I can use"""
    while True:
        try:
            val = _type(input(prompt))
            return val
        except ValueError:
            pass
