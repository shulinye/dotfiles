#!/usr/bin/python

import sys

__all__ = ['coerced_input', 'gen_translation_table']

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

if sys.version_info.major <= 2:
    from string import maketrans
    def gen_translation_table(intake,output):
        """Generates translation table: for python 2"""
        return maketrans(intake,output)
else:
    def gen_translation_table(intake,output):
        """Generates translation table: for python 3"""
        return dict(zip(map(ord,intake), output))
