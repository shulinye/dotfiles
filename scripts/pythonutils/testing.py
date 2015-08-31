import datetime
import logging
import __main__

import errno
from functools import wraps, update_wrapper, partial
import inspect
import os
import signal
import traceback
import types

from .autorepr import autorepr

__all__ = ['testing_setup', 'sloppy_run', 'typecheck', 'type_validate', 'TheShowMustGoOn', 'limited_globals', 'Timeout']

def testing_setup():
    """Default setup for logging"""
    LOG_FILENAME =  getattr(__main__,"__file__","unknown.").split('.')[0] + "." + datetime.datetime.now().isoformat() + ".log"
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)


def sloppy_run(func, *args, **kwargs):
    """Runs a function, catching all exceptions
    and writing them to a log file."""
    try:
        return func(*args, **kwargs)
    except:
        logging.exception(func.__name__ + str(args) + str(kwargs))
sloppy_run.export_control = True

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

def mod_docstring(func, val):
    if func.__doc__ : fuc.__doc__ += "\n %s" % val
    else: func .__doc__ = val
    func.export_control = True

def yield_positional(params):
    for i in params:
        if i.kind == inspect.Parameter.POSITIONAL_ONLY:
            yield i
        elif i.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            yield i
        elif i.kind == inspect.Parameter.VAR_POSITIONAL:
            while True:
                yield i
        else:
            raise StopIteration

def type_validate(func):
    """Validates types for functions, using
    function annotations"""
    params = inspect.signature(func).parameters
    @wraps(func)
    def decorated(*args, **kwargs):
        positional = yield_positional(params.values())
        for i in args:
            try:
                j = next(positional)
                if j.annotation != inspect._empty and not isinstance(i, j.annotation):
                    raise TypeError("Input of incorrect type:\n expected %r for %s, got %r" % (j.annotation, j.name, type(i)))
            except StopIteration:
                raise TypeError("Too many positional arguments")
        for i in kwargs:
            if params[i].annotation != inspect._empty and kwargs[i] != params[i].default and not isinstance(kwargs[i], params[i].annotation):
                raise TypeError("Input of incorrect type:\n expected %r for %s, got %r" % (params[i].annotation, params[i].name, type(i)))
        ret = func(*args, **kwargs)
        if 'return' in func.__annotations__ and not isinstance(ret, func.__annotations__['return']):
            raise TypeError("%s returned item not of type %r" % (func.__qualname__, func.__annotations__['return']))
        return ret
    mod_docstring(decorated, "type validation is on")
    return decorated

@autorepr
class TheShowMustGoOn(object):
    """Catches exceptions, writes them to log file.
    After all, the show must go on.
    
    Works as:
        - a function decorator
        
        @TheShowMustGoOn()
        def f():
            raise ValueError
        
        - a class decorator (decorates all the methods of the class)
        @TheShowMustGoOn()
        class Merp(object):
            def method1():
                raise ValueError
        
        -Context manager
        with TheShowMustGoOn():
            raise ValueError"""
    def __init__(self, *, level = logging.DEBUG, prefix=""):
        self.level = level
        self.prefix = prefix
    def __call__(self, obj):
        if inspect.isclass(obj):
            for name, val in inspect.getmembers(obj, inspect.isroutine):
                if hasattr(val, '__call__'):
                    setattr(obj, name, self(val))
            return obj
        @wraps(obj)
        def decorated(*args, **kwargs):
            logging.log(self.level, self.prefix + "calling '%s'(%r,%r)", obj.__qualname__, args, kwargs)
            try:
                ret = obj(*args, **kwargs)
            except:
                logging.exception("Got exception in %s."  % func.__qualname__)
                return None
            else:
                logging.log(self.level, "Got results: %r", ret)
                return ret
        mod_docstring(decorated, 'Wrapped with TheShowMustGoOn')
        return decorated
    def __enter__(self):
        pass
    def __exit__(self, etype, value, trace):
        if etype is not None:
            logging.error("Got exception:\n" + ''.join(traceback.format_exception(etype, value, trace)))
            return True #swallow errors
        logging.log(self.level, "No errors")

def limited_globals(func = None, *, allowed_modules = None):
    """Limit a function's access to globals (__builtins__ allowed though)"""
    if func is None: return partial(limited_globals, allowed_modules=allowed_modules)
    if allowed_modules is None:
        allowed_modules = set('__builtins__')
    else:
        allowed_modules = {getattr(i,"__name__", i) for i in allowed_modules}
        allowed_modules.add('__builtins__')
    g = {k:v for k,v in func.__globals__.items() if k in allowed_modules}
    new_func = types.FunctionType(func.__code__, g, func.__name__, func.__defaults__, func.__closure__)
    update_wrapper(new_func, func)
    mod_docstring(new_func, "Limited globals: " + ', '.join(allowed_modules))
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

    Unix only (relies on signal.SIGALRM) and not thread-safe.
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
        self.old_handle = signal.signal(signal.SIGALRM, self.handle)
        signal.alarm(self.seconds)
    def __exit__(self, etype, value, traceback):
        signal.alarm(0)
        signal.signal(signal.SIGALRM, self.old_handle)
    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            old_handle = signal.signal(signal.SIGALRM, self.handle)
            signal.alarm(self.seconds)
            try:
                ret = func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handle)
            return ret
        if decorated.__doc__: decorated.__doc__ += "\n Timeout: %s" % self.seconds
        else: decorated.__doc__ = "With timeout: %s" % self.seconds
        return decorated
