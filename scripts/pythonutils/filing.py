#!/usr/bin/python3

import os
import shutil
import sys
import tempfile
import argparse

__all__ = ['infile_simple', 'outfile']

class infile_simple(object):
    def __init__(self, file_name = None, require_input=False):
        self.file_name = file_name
        if require_input and self.file_name is None:
            if sys.stdin.isatty():
                raise RuntimeError("Input Expected")
    def __enter__(self):
        if self.file_name is None:
            self.f = sys.stdin
        else:
            self.f = open(self.file_name)
        return self.f
    def __exit__(self, etype, value, traceback):
        if self.f is not sys.stdin:
            self.f.close()
    def __getattr__(self, val):
        return getattr(self.f, val) # pass on other attributes to the underlying filelike object
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, str(self.file_name))

class outfile(object):
    def __init__(self, file_name=None, *, infile_name=None, with_temp=False, noclobber=False):
        self.noclobber = noclobber
        if self.noclobber and file_name and infile_name == file_name:
            raise RuntimeError("That makes no sense.")
        if noclobber and os.path.exists(file_name):
            raise RuntimeError("Sorry, file already exists.")
        if file_name and infile_name == file_name:
            self.with_temp = True
        else:
            self.with_temp = with_temp
        if with_temp and file_name is None and infile_name is not None:
            self.file_name = infile_name
        else:
            self.file_name = file_name
        self.infile_name = infile_name
    def __enter__(self):
        if self.with_temp:
            self.f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
            self.tmppath = self.f.name
        elif self.file_name is None:
            self.f = sys.stdout
            self.tmppath = None
        else:
            self.f = open(self.file_name, 'w')
            self.tmppath = None
        return self.f
    def __exit__(self, etype, value, traceback):
        if etype is None and self.tmppath:
            # If I got no errors, go ahead and copy
            self.f.flush()
            shutil.copyfile(self.tmppath, self.file_name)
        if self.f is not sys.stdout:
            self.f.close()
        if self.path:
            os.remove(self.tmppath)
    def __getattr__(self, val):
        return getattr(self.f, val)
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, str(self.file_name))

class MyParser(argparse.ArgumentParser): #uh, rename this?
    def __init__(self, *args, **kwargs):
        super().__(*args, **kwargs)
