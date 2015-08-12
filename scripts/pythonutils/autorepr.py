#!/usr/bin/python3

from functools import partial
import inspect
import types

__all__ = ['autorepr']

def autorepr(obj=None, *, params=None):
    """Function that automagically gives you a __repr__.
    If no params are given, inspects __init__
    Can be used as a class decorator or by setting
    __repr__ = autorepr"""
    if obj is None: return partial(autorepr, params = params)
    if params:
        discard_first = False
    elif hasattr(obj, '__slots__'):
        params = obj.__slots__
        discard_first = False
    else:
        sig = inspect.signature(obj.__init__)
        params = sig.parameters
        discard_first = True
    if isinstance(obj,type): #I'm being used as a decorator
        if discard_first: params = list(params)[1:] #drop the first argument, that's self
        s = "def __repr__(self):\n    return '%s(" + ", ".join(["%s=%r"]*(len(params)))
        s += ")' % (self.__class__.__name__, "
        s += ', '.join("'{0}', self.{0}".format(i) for i in params) + ')'
        scope = {}
        exec(s, scope)
        setattr(obj, '__repr__', scope['__repr__'])
        return obj
    else: #Being a normal function here :P
        return "%s(%s)" % (obj.__class__.__name__, ", ".join("%s=%r" % (i, getattr(obj,i)) for i in params))
