#!/usr/bin/python3

import os
import sys

def validate_init(self, *, stdout=None, stderr=None, noclobber=False, use_temp=False, mode='w'):
    self.use_temp = use_temp
    self.mode = mode
    self.noclobber = nonclobber
    if noclobber:
        for i in stdout, stderr:
            if i is not None and os.path.lexists(i):
                raise RuntimeError("%s already exists", %s)
    self.stdout = stdout
    self.stderr = stderr

class RedirectStreams(object):
    """Redirect the standard streams somewhere"""
    __init__ = validate_init
    def __enter__(self):
        self.files = []
        if self.stdout is None:
            self.stdout = sys.stdout
        else:
            f = open(self.stdout, 'w')
            self.stdout = f
            self.files.append(f)
        if self.stderr is None:
            self.stderr = sys.stderr
        elif self.stderr == self.stdout:
            self.stderr = f
        else:
            f = open(self.stderr, 'w')
            self.stderr = f
            self.files.append(f)
        sys.stdout.flush() ; sys.stderr.flush()
        sys.stdout, sys.stderr = self.stdout, self.stderr
    def __exit__(self, etype, value, trace):
        sys.stdout.flush() ; sys.stderr.flush()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        for i in self.files: i.close()
    def __repr__(self):
        return "%s(stdout=%s, stderr=%s)" % (self.__class__.__name__, str(self.stdout), str(self.stderr))

class Tee(object):
    def __init__(*outputs):
        self.outputs = outputs
    def write(self, val):
        for i in self.outputs: i.write(val)
    def flush(self):
        for i in self.outputs: i.flush()
    def writelines(self, lines):
        for i in self.outputs: i.writelines(lines)
    def __repr__(self):
        return self.__class__.__name__ + "\n\t".join(repr(i) for i in self.outputs)

class TeeStreams(object):
    """Tee the standard streams to a file."""
    __init__ = validate_init
    def __enter__(self):
        self.files = []
        if self.stdout is None:
            self.stdout = sys.stdout
        else:
            f = open(self.stdout, 'w')
            self.stdout = Tee(sys.stdout, f)
            self.files.append(f)
        if self.stderr is None:
            self.stderr = sys.stderr
        elif self.stderr == self.stdout:
            self.stderr = Tee(sys.stderr, f)
        else:
            f = open(self.stderr, 'w')
            self.stderr = Tee(sys.stderr, f)
            self.files.append(f)
        sys.stdout.flush() ; sys.stderr.flush()
        sys.stdout, sys.stderr = self.stdout, self.stderr
    def __exit__(self, etype, value, trace):
        sys.stdout.flush() ; sys.stderr.flush()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        for i in self.files: i.close()
    def __repr__(self):
        return "%s(stdout=%s, stderr=%s)" % (self.__class__.__name__, str(self.stdout), str(self.stderr))
