import logging
import __main__
import datetime

LOG_FILENAME =  getattr(__main__,"__file__","unknown.").split('.')[0] + "." + datetime.datetime.now().isoformat() + ".log"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

from functools import wraps, update_wrapper, partial
from inspect import signature
import types

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
        if callable(val):
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

