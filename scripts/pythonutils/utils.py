#/usr/bin/env python3

import argparse
import inspect

def nonempty(item):
    return item if item != inspect._empty else None

class UtilsParser(argparse.ArgumentParser):
    def __init__(self, *args, funclist = None,  **kwargs):
        super().__init__(*args, **kwargs)
        self.subparsers = self.add_subparsers(parser_class=argparse.ArgumentParser)
        self.funclist = []
        self.has_kwargs = {}
        self.mapping = {}
        if funclist: self.add_functions(*funclist)
    def add_functions(self, *funclist):
        self.funclist.extend(funclist)
        for func in funclist:
            print(func.__name__)
            subparser = self.subparsers.add_parser(func.__name__)
            subparser.set_defaults(which=func.__name__)
            params = inspect.signature(func).parameters.values()
            for p in params:
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
    def parse_args(self, *args, **kwargs):
        args, remainder = self.parse_known_args(*args, **kwargs)

    #//TODO: overwrite parse_args
