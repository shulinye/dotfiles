#!/usr/bin/python3

from functools import partial
import inspect
import types

def autorepr(obj = None, *, params = None):
    """Function that automagically gives you a __repr__.
    If no params are given, inspects __init__
    Can be used as a class decorator or by setting
    __repr__ = autorepr"""
    if obj is None: return partial(autorepr, params = params)
    if not params:
        sig = inspect.signature(obj.__init__)
        params = sig.parameters
        inspected = True
    if isinstance(obj,type): #I'm being used as a decorator
        if inspected: params = list(params)[1:] #drop the first argument, that's self
        s = "def __repr__(self):\n    return '%s(" + ", ".join(["%s"]*(len(params)))
        s += ")' % (self.__class__.__name__, "
        s += ', '.join("'%s=' + repr(self.%s)" % (i, i) for i in params) + ')'
        exec(s, locals())
        setattr(obj, '__repr__', locals()['__repr__'])
        return obj
    else: #Being a normal function here :P
        return "%s(%s)" % (obj.__class__.__name__, ", ".join("%s=%s" % (i, repr(getattr(obj,i))) for i in params))
