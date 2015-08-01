#!/usr/bin/python3

import inspect

def autorepr(instance):
    sig = inspect.signature(instance.__init__)
    param = iter(sig.parameters)
    return "%s(%s)" % (instance.__class__.__name__, ", ".join("%s=%s" % (i, getattr(instance,i)) for i in param))
