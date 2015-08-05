import datetime
import logging
import __main__

import errno
from functools import wraps, update_wrapper, partial
import inspect
import os
import signal
import types

from .autorepr import autorepr

def setup():
    LOG_FILENAME =  getattr(__main__,"__file__","unknown.").split('.')[0] + "." + datetime.datetime.now().isoformat() + ".log"
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)


def sloppyRun(func, *args, **kwargs):
    """Runs a function, catching all exceptions
    and writing them to a log file."""
    try:
        return func(*args, **kwargs)
    except:
        logging.exception(func.__name__ + str(args) + str(kwargs))
sloppyRun.sloppy = True

def typecheck(obj, *args):
    """Check type of nested objects"""
    if isinstance(obj, args[0]):
        if len(args) == 1:
            return True
        if hasattr(args[0], "__iter__"):
            for i in obj:
                if not typecheck(i, *args[1:]):
                    return False
            return True
    return False

def theShowMustGoOn(func = None, level = logging.DEBUG, prefix=""):
    """Decorator. Catches exceptions, writes them to log file."""
    if func is None: return partial(theShowMustGoOn, level=level, prefix=prefix)
    @wraps(func)
    def decorated(*args, **kwargs):
        logging.log(level, prefix + "calling '%s'(%r,%r)", func.__qualname__, args, kwargs)
        try:
            ret = func(*args, **kwargs)
        except:
            logging.exception("Got exception.")
            return None
        else:
            logging.log(level, "Got results: %r", ret)
            return ret
    if decorated.__doc__ : decorated.__doc__ += "\n Wrapped with theShowMustGoOn"
    else: decorated.__doc__ = "Wrapped with theShowMustGoOn"
    decorated.export_control = True
    return decorated

def thisClassMustGoOn(cls = None, level = logging.DEBUG, prefix=""):
    if cls is None: return partial(thisClassMustGoOn, level=level, prefix=prefix)
    for key, val in vars(cls).items():
        if hasattr(val, '__call__'):
            setattr(cls, key, theShowMustGoOn(val, level=level, prefix=prefix))
    return cls

def limited_globals(func = None, *, allowed_modules = None):
    if func is None: return partial(limited_globals, allowed_modules=allowed_modules)
    if allowed_modules is None:
        allowed_modules = set('__builtins__')
    else:
        allowed_modules = {getattr(i,"__name__", i) for i in allowed_modules}
        allowed_modules.add('__builtins__')
    g = {k:v for k,v in func.__globals__.items() if k in allowed_modules}
    new_func = types.FunctionType(func.__code__, g, func.__name__, func.__defaults__, func.__closure__)
    update.wrapper(new_func, func)
    if new_func.__doc__: new_func.__doc__ += "\n Limited globals: " + ", ".join(allowed_modules)
    else: new_func.__doc__ = "Limited globals: " + ', '.join(allowed_modules)
    new_func.export_control = True
    return new_func

@autorepr
class Timeout(object):
    """Run a function or a block of code for a certain amount of time.
    Raises TimeoutError if time exceeded.

    Can be used as a context manager or a decorator

    with Timeout():
        stuff

    @Timeout()
    def function():
        pass
    """
    def __init__(self, *, seconds=5, error_message=os.strerror(errno.ETIME), loglevel = None):
        self.seconds = seconds
        self.error_message = error_message
        self.loglevel = None
    def handle(self, signum, frame):
        if self.loglevel is not None:
            logging.log(self.loglevel, repr(inspect.getframeinfo(frame)))
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle)
        signal.alarm(self.seconds)
    def __exit__(self, etype, value, traceback):
        signal.alarm(0)
    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            signal.signal(signal.SIGALRM, self.handle)
            signal.alarm(self.seconds)
            try:
                ret = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return ret
        if decorated.__doc__: decorated.__doc__ += "\n Timeout: %s" % self.seconds
        else: decorated.__doc__ = "With timeout: %s" % self.seconds
        return decorated
