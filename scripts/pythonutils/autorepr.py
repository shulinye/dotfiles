#!/usr/bin/python3

from collections import OrderedDict
from functools import partial
from ordered_set import OrderedSet
import inspect
import itertools
import types

from .utils import walk_getattr

__all__ = ['autoinit', 'autorepr', 'TotalCompareByKey']


def autoinit(obj=None, *args, params=None, **kwargs):
    """Takes __slots__ and _slots and writes an __init__
    
    Can be used as a class decorator, or by setting
    __init__ = autoinit"""
    if obj is None: return partial(autoinit, params=params)
    if params:
        pass
    elif hasattr(obj, '__slots__'):
        params = OrderedSet(itertools.chain.from_iterable(walk_getattr(obj, '__slots__')))
    elif hasattr(obj, '_slots'):
        params = OrderedSet(itertools.chain.from_iterable(walk_getattr(obj, '_slots')))
    else:
        raise RuntimeError("Can't autocreate __init__, please supply '__slots__' or '_slots'")
    if inspect.isclass(obj): #I'm being used as a decorator
        s = ["def __init__(self,{}):".format(", ".join(i for i in params))]
        s.extend("self.{0} = {0}".format(i) for i in params)
        scope = {}
        exec('\n    '.join(s), scope)
        setattr(obj, '__init__', scope['__init__'])
        return obj
    else:
        signature = inspect.Signature(inspect.Parameter(i, inspect.Parameter.POSITIONAL_OR_KEYWORD) for i in params)
        signature.bind(*args, **kwargs)
        for p, val in itertools.chain(zip(params, args), kwargs.items()):
            setattr(obj, p, val)

def autorepr(obj=None, *, params=None):
    """Function that automagically gives you a __repr__.
    If no params are given, uses __slots__, _slots, and at last resort,
    inspects __init__

    Can be used as a class decorator or by setting
    __repr__ = autorepr"""
    if obj is None: return partial(autorepr, params = params)
    discard_first = False
    if params:
        pass
    elif hasattr(obj, '__slots__'):
        params = OrderedSet(itertools.chain.from_iterable(walk_getattr(obj, '__slots__')))
    elif hasattr(obj, '_slots'):
        params = OrderedSet(itertools.chain.from_iterable(walk_getattr(obj, '_slots')))
    else:
        sig = inspect.signature(obj.__init__)
        params = sig.parameters
        discard_first = True
    if inspect.isclass(obj): #I'm being used as a decorator
        if discard_first: params = list(params)[1:] #drop the first argument, that's self
        s = ["def __repr__(self):\n    return '%s(" + ", ".join(["%s=%r"]*(len(params)))]
        s.append(")' % (self.__class__.__name__, ")
        s.append(', '.join("'{0}', self.{0}".format(i) for i in params) + ')')
        scope = {}
        exec("".join(s), scope)
        setattr(obj, '__repr__', scope['__repr__'])
        return obj
    else: #Being a normal function here :P
        return "%s(%s)" % (obj.__class__.__name__, ", ".join("%s=%r" % (i, getattr(obj,i)) for i in params))

class TotalCompareByKey(object):
    """Writes all comparison methods using one key"""
    __slots__ = ['key', 'check_type']
    def __init__(self, key, *, check_type=True):
        self.key = key
        self.check_type = check_type
    def __call__(self, cls):
        orderings = {'__lt__': '<',
                     '__le__': '<=',
                     '__gt__': '>',
                     '__ge__': '>=',
                     '__eq__': '==',
                     '__ne__': '!='}
        for dunder, symbol in orderings.items():
            if dunder in cls.__dict__: continue
            s = ["def {dunder}(self, other):".format(dunder=dunder)]
            if self.check_type:
                s.append("if not isinstance(other, self.__class__):")
                s.append("    return NotImplemented")
            s.append("return self.{k} {symbol} other.{k}".format(k=self.key, symbol=symbol))
            scope = {}
            exec("\n    ".join(s), scope)
            setattr(cls, dunder, scope[dunder])
        return cls
