#/usr/bin/env python

__all__ = ['NullArgument', 'vgetattr']

from contextlib import suppress

class NullArgument(object):
    """Singleton. Use as a default argument when
    you want None to be a possible argument"""
    pass

def vgetattr(obj, *attrs, default=NullArgument):
    """Vectorized getattr. Returns first attribute found, or default.
        If default not given, raises AttributError"""
    for i in attrs:
        with suppress(AttributeError):
            return getattr(obj, i)
    if default is NullArgument:
        raise AttributeError("%r has none of these attributes: %s" % (type(obj), ", ".join(attrs)))
    return default

def walk_getattr(klass, attr):
    """Walks the mro backwards, grabbing
    the attr from each class that has it"""
    for cls in reversed(klass.__mro__):
        with suppress(AttributeError):
            yield getattr(cls, attr)

