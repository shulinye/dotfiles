import logging
import __main__
LOG_FILENAME =  getattr(__main__,"__file__",".").split('.')[0] +".log"
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)


def sloppyRun(func, *args, **kwargs):
    """Runs a function, catching all exceptions
    and writing them to a log file."""
    try:
        return func(*args, **kwargs)
    except:
        logging.exception(func.__name__ + str(args) + str(kwargs))


def typecheck(obj, *args):
    if isinstance(obj, args[0]):
        if len(args) == 1:
            return True
        if hasattr(args[0], "__iter__"):
            for i in obj:
                if not typecheck(i, *args[1:]):
                    return False
            return True
    return False
        
