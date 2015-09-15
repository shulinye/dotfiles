#!/usr/bin/python

from functools import wraps
import sys

__all__ = ['coerced_input', 'direct_input', 'gen_translation_table']

if sys.version_info.major <= 2:
    input = raw_input

class DirectInput(object):
    """Read input directly from the user, no matter what
    
    Use as:
        -> normal function:
        
            x = direct_input(prompt)

        -> decorator:
            
            @direct_input
            def f():
                x = input('prompt') #Even when piped, will ask user
        
        -> context manager
        
            with direct_input:
                x = input('prompt')"""
    def __init__(self):
        self.inputfile = 'CON:' if sys.platform in ('win32', 'cygwin') else '/dev/tty'
    def __enter__(self):
        self.old_stdin = sys.stdin
        sys.stdin.flush()
        sys.stdin = open(self.inputfile)
    def __exit__(self, etype, value, trace):
        sys.stdin.flush()
        sys.stdin = self.old_stdin
    def __call__(self, obj):
        if callable(obj): # act as decorator
            @wraps(obj)
            def decorated(*args, **kwargs):
                with self:
                    return obj(*args, **kwargs)
            return decorated
        else:
            with self:
                return input(obj)
    def __repr__(self):
        return "<%s for %s>" % (self.__class__.__name__, {'CON:': 'Windows', '/dev/tty': 'Unix'}[self.inputfile])

direct_input = DirectInput()

def coerced_input(prompt, type_ = float):
    """Continue asking user for input
    until they give one that's of a type
    I can use"""
    while True:
        try:
            return type_(input(prompt))
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
