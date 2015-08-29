#!/usr/bin/python3

from functools import partial
import inspect
import types

__all__ = ['autoinit', 'autorepr', 'total_compare_by_key']

def autoinit(cls=None, *, params=None):
    """Takes __slots__ and _slots and writes an __init__"""
    if cls is None: return partial(autoinit, params=params)
    if params is None:
        try:
            params = getattr(cls, '__slots__') if hasattr(cls, '__slots__') else getattr(cls, '_slots')
        except AttributeError:
            raise RuntimeError("Can't autocreate __init__, please supply '__slots__' or '_slots'")
    s = "def __init__(self,{}):\n    ".format(", ".join(i for i in params))
    s += "\n    ".join("self.{0} = {0}".format(i) for i in params)
    scope = {}
    exec(s, scope)
    setattr(cls, '__init__', scope['__init__'])
    return cls

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
    if inspect.isclass(obj): #I'm being used as a decorator
        if discard_first: params = list(params)[1:] #drop the first argument, that's self
        s = ["def __repr__(self):\n    return '%s(" + ", ".join(["%s=%r"]*(len(params)))]
        s.append(")' % (self.__class__.__name__, ")
        s.append(', '.join("'{0}', self.{0}".format(i) for i in params) + ')')
        s = "".join(s)
        scope = {}
        exec(s, scope)
        setattr(obj, '__repr__', scope['__repr__'])
        return obj
    else: #Being a normal function here :P
        return "%s(%s)" % (obj.__class__.__name__, ", ".join("%s=%r" % (i, getattr(obj,i)) for i in params))

def total_compare_by_key(cls=None, *, key=None, check_type=True):
    """Total ordering, based on one attribute only"""
    if cls is None: return partial(order_by_key, key=key)
    if key is None: raise RuntimeError("Key for ordering required")
    orderings = {'__lt__': '<',
                 '__le__': '<=',
                 '__gt__': '>',
                 '__ge__': '>=',
                 '__eq__': '==',
                 '__ne__': '!='}
    for dunder, symbol in orderings.items():
        s = ["def {dunder}(self, other):".format(dunder=dunder)]
        if check_type:
            s.append("if not isinstance(other, self.__class__):")
            s.append("    raise TypeError('unorderable types, %s {} %s' % (type(self).__name__, type(other).__name__))".format(symbol))
        s.append("return self.{k} {symbol} other.{k}".format(k=key, symbol=symbol))
        s = "\n    ".join(s)
        scope = {}
        exec(s, scope)
        setattr(cls, dunder, scope[dunder])
    return cls
