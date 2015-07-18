import logging
import __main__
import datetime

LOG_FILENAME =  getattr(__main__,"__file__","unknown.").split('.')[0] + "." + datetime.datetime.now().isoformat() + ".log"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

from functools import wraps, partial
from inspect import signature

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
    sig = signature(func)
    @wraps(func)
    def decorated(*args, **kwargs):
        sig.bind(*args, **kwargs) #Have the same signature as the original function?
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
    decorated.sloppy = True
    return decorated

def thisClassMustGoOn(cls = None, level = logging.DEBUG, prefix=""):
    if cls is None: return partial(thisClassMustGoOn, level=level, prefix=prefix)
    for key, val in vars(cls).items():
        if callable(val):
            setattr(cls, key, theShowMustGoOn(val, level=level, prefix=prefix))
    return cls
