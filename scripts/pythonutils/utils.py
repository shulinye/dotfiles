#/usr/bin/env python

__all__ = ['NullArgument', 'vgetattr', 'walk_getattr']

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

def walk_getattr(klass, *attrs, reverse=False):
    """Walks the mro, grabbing
    the attr from each class that has it"""
    mro = reversed(klass.__mro__) if reverse else klass.__mro__
    for cls in mro:
        with suppress(AttributeError):
            yield vgetattr(cls, *attrs)

