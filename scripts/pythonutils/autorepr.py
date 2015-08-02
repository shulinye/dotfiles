#!/usr/bin/python3

import inspect

def autorepr(instance, *params):
    if not params:
        sig = inspect.signature(instance.__init__)
        params = iter(sig.parameters)
    return "%s(%s)" % (instance.__class__.__name__, ", ".join("%s=%s" % (i, repr(getattr(instance,i))) for i in params))
