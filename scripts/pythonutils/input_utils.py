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

if sys.platform not in ('win32', 'cygwin'):
    import signal
    __all__.append('input_with_timeout')
    def input_with_timeout(prompt, timeout):
        """Times out input after a certain number of seconds. Linux/Mac version, uses signals"""
        old_handler = signal.signal(signal.SIGALRM, lambda x,y: (_ for _ in '').throw(TimeoutError))
        signal.alarm(timeout)
        try:
            return input(prompt)
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
    #//TODO: perhaps a windows variant?

if sys.version_info.major <= 2:
    from string import maketrans
    def gen_translation_table(intake,output):
        """Generates translation table: for python 2"""
        return maketrans(intake,output)
else:
    def gen_translation_table(intake,output):
        """Generates translation table: for python 3"""
        return dict(zip(map(ord,intake), output))
