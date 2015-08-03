#!/usr/bin/python3

from functools import partial
import inspect
import types

def autorepr(obj = None, *, params = None):
    if obj is None: return partial(autorepr, params = params)
    if not params:
        sig = inspect.signature(obj.__init__)
        params = sig.parameters
    if isinstance(obj,type): #I'm being used as a decorator
        if 'self' in params:
            params = [i for i in params if i !='self']
        s = "def __repr__(self):\n    return '%s(" + ", ".join(["%s"]*(len(params)))
        s += ")' % (self.__class__.__name__, "
        s += ', '.join("'%s=' + repr(self.%s)" % (i, i) for i in params) + ')'
        exec(s, locals())
        setattr(obj, '__repr__', locals()['__repr__'])
        return obj
    else: #Being a normal function here :P
        return "%s(%s)" % (obj.__class__.__name__, ", ".join("%s=%s" % (i, repr(getattr(obj,i))) for i in params))
