#!/usr/bin/python3

import os
import shutil
import sys
import tempfile

class infile(object):
    def __init__(self, file_name=None):
        self.file_name = file_name
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

class outfile(object):
    def __init__(self, file_name=None, *, infile_name=None, inplace=False):
        self.file_name = file_name
        self.infile_name = infile_name
        self.inplace = inplace
    def __enter__(self):
        if self.inplace or (self.file_name and self.file_name == self.infile_name):
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
        # If got no errors...
        if etype is None and self.tmppath:
            self.f.flush()
            shutil.copy(self.tmppath, self.infile_name)
        if self.f is not sys.stdout:
            self.f.close()
        if self.path:
            os.remove(self.tmppath)
    def __getattr__(self, val):
        return getattr(self.f, val)
