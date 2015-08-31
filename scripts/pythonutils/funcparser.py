#/usr/bin/env python3

import argparse
import inspect
import __main__

__all__ = ['FuncParser']

def nonempty(item):
    return item if item != inspect._empty else None

class FuncParser(argparse.ArgumentParser):
    def __init__(self, *args, funclist=None, description=None, **kwargs):
        if description is None:
            description = inspect.getdoc(__main__)
        super().__init__(*args, description=description, **kwargs)
        self.subparsers = self.add_subparsers(parser_class=argparse.ArgumentParser)
        self.has_kwargs = {}
        self.mapping = {}
        self.param_map = {}
        if funclist: self.add_functions(*funclist)
    def _get_kwargs(self):
        s = super()._get_kwargs()
        s.append(('funclist', list(i.__qualname__ for i in self.mapping.values()) if self.mapping else None))
        return s
    def add_functions(self, *funclist):
        for func in funclist:
            self.mapping[func.__name__] = func
            subparser = self.subparsers.add_parser(func.__name__, description=inspect.getdoc(func))
            subparser.set_defaults(which_func=func.__name__)
            params = inspect.signature(func).parameters
            self.param_map[func.__name__] = params
            for p in params.values():
                if p.kind == inspect.Parameter.POSITIONAL_ONLY:
                    subparser.add_argument(p.name, type=nonempty(p.annotation), nargs=1)
                elif p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                    subparser.add_argument('--' + p.name, type=nonempty(p.annotation), default=p.default, dest = 'kw_' + p.name)
                    subparser.add_argument(p.name, type=nonempty(p.annotation), default=p.default, nargs='?')
                elif p.kind == inspect.Parameter.VAR_POSITIONAL:
                    subparser.add_argument(p.name, type=nonempty(p.annotation), nargs='*', default=[])
                elif p.kind == inspect.Parameter.KEYWORD_ONLY:
                    subparser.add_argument("--" + p.name, type=nonempty(p.annotation), default=p.default)
                elif p.kind == inspect.Parameter.VAR_KEYWORD:
                    self.has_kwargs[func.__name__] = p.annotation
    def parse_known_args(self, *args, **kwargs):
        args, remainder = super().parse_known_args(*args, **kwargs)
        self.collapse_kwargs(args)
        return args, remainder
    def collapse_kwargs(self, args):
        missing = []
        doubles = []
        dict_args = dict(vars(args))
        func = self.mapping[args.which_func]
        params = self.param_map[args.which_func]
        for k in dict_args:
            if k.startswith('kw_'):
                dest = k[3:]
                if dict_args[k] == dict_args[dest]:
                    if dict_args[k] == inspect._empty:
                        missing.append(dest)
                    else:
                        delattr(args, k)
                else:
                    if dict_args[k] == params[dest].default:
                        delattr(args, k)
                    elif dict_args[dest] == params[dest].default:
                        setattr(args, dest, dict_args[k])
                        delattr(args, k)
                    else:
                        doubles.append(dest)
        error_msg = []
        if missing:
            error_msg.append('Missing %d required arguments: %s' % (len(missing), ', '.join(missing)))
        if doubles:
            error_msg.append('Arguments supplied twice: %s' % ', '.join(doubles))
        if error_msg:
            self.error("\n".join(error_msg))
    #//TODO: deal with kwargs
