#/usr/bin/env python3

import argparse
import inspect

class UtilsParser(argparse.ArgumentParser):
    def __init__(self, mapping, *args, **kwargs):
        parser = super().__init__(*args, **kwargs)
        subparsers = parser.add_subparsers()
        for name, func in mapping.items():
            subparser = subparsers.add_parser(name)
            subparser.set_defaults(which=name)
            params = inspect.signature(func).parameters
            for i,j in func.__annotations__.items():
                subparser.add_argument("--" + i, type=j, default=params[i].default)

