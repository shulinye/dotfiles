#!/usr/bin/python3

__all__ = ['color', 'ColorBlock']

import colorama
from functools import wraps
from .autorepr import autoinit, autorepr

colorama.init()

class color(object):
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

@autorepr
@autoinit
class ColorBlock(object):
    __slots__= ('colorcode',)
    def __enter__(self):
        print(getattr(color, self.colorcode, self.colorcode), end='')
    def __exit__(self, etype, val, trace):
        print(colorama.Style.RESET_ALL, end='')
    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
            return ret
        return decorated
