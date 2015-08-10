#!/usr/bin/python3

import os
import shutil
import sys
import tempfile

from .autorepr import autorepr
__all__ = ['RedirectStreams', 'TeeStreams', 'Tee', 'LoggerFilelike', 'LogStderr']

def validate_init(self, *, stdout=None, stderr=None, noclobber=False, use_temp=False, mode='w'):
    self.use_temp = use_temp
    self.mode = mode
    self.noclobber = noclobber
    if noclobber:
        for i in stdout, stderr:
            if i is not None and os.path.lexists(i):
                raise RuntimeError("%s already exists" % i)
    self.stdout = stdout
    self.stderr = stderr

@autorepr
class RedirectStreams(object):
    """Redirect the standard streams somewhere"""
    __init__ = validate_init
    def reset(self):
        self.files = [None,None]
        self.tmppaths = [None,None]
    def __enter__(self):
        self.reset()
        if self.stdout is not None:
            if self.noclobber and os.path.lexists(self.stdout):
                raise RuntimeError("%s already exists" % self.stdout)
            if self.use_temp:
                self.files[0] = tempfile.NamedTemporaryFile(delete=False)
                self.tmppaths[0] = self.files[0].name
            else:
                self.files[0] = open(self.stdout, self.mode)
            sys.stdout.flush()
            sys.stdout = self.files[0]
        if self.stderr is None:
            pass
        elif self.stderr == self.stdout:
            sys.stderr.flush()
            sys.stderr = self.files[0]
        else:
            if self.noclobber and os.path.lexists(self.stderr):
                raise RuntimeError("%s already exists" % self.stderr)
            if self.use_temp:
                self.files[1] = tempfile.NamedTemporaryFile(delete=False)
                self.tmppaths[1] = self.files[1].name
            else:
                self.files[1] = open(self.stderr, self.mode)
            sys.stderr.flush()
            sys.stderr = self.files[1]
    def __exit__(self, etype, value, trace):
        sys.stdout.flush() ; sys.stderr.flush()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        if self.use_temp:
            for tmpfile, path, dest in zip(self.files, self.temppaths, [self.stdout, self.stderr]):
                if tmpfile:
                    tmpfile.flush()
                    shutil.copyfile(path, dest)
                    os.remove(path)
        for i in self.files:
            if i is not None: i.close()
        self.reset()

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

@autorepr
class TeeStreams(object):
    """Tee the standard streams to a file."""
    __init__ = validate_init
    def reset(self):
        self.tees = [None, None]
        self.files = [None, None]
        self.tmppaths = [None, None]
    def __enter__(self):
        self.reset()
        if self.stdout is not None:
            if self.noclobber and os.path.lexists(self.stdout):
                raise RuntimeError("%s already exists" % self.stdout)
            if self.use_temp:
                self.files[0] = tempfile.NamedTemporaryFile(delete=False)
                self.tmppaths[0] = self.files[0].name
            else:
                self.files[0] = open(self.stdout, self.mode)
            self.tees[0] = Tee(sys.stdout, self.files[0])
            sys.stdout.flush()
            sys.stdout = self.tees[0]
        if self.stderr is None:
            pass
        elif self.stderr == self.stdout:
            self.tees[1] = Tee(sys.stderr, f)
            sys.stderr.flush()
            sys.stderr = self.tees[1]
        else:
            if self.noclobber and os.path.lexists(self.stderr):
                raise RuntimeError("%s already exists" % self.stderr)
            if self.use_temp:
                self.files[1] = tempfile.NamedTemporaryFile(delete=False)
                self.tmppaths[1] = self.files[1].name
            else:
                self.files[1] = open(self.stderr, self.mode)
            self.tees[1] = Tee(sys.stderr, self.files[1])
            sys.stderr.flush()
            sys.stderr = self.tees[1]
    def __exit__(self, etype, value, trace):
        sys.stdout.flush() ; sys.stderr.flush()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        if self.use_temp:
            for tmpfile, path, dest in zip(self.files, self.temppaths, [self.stdout, self.stderr]):
                if tmpfile:
                    tmpfile.flush()
                    shutil.copyfile(path, dest)
                    os.remove(path)
        for i in self.files:
            if i is not None: i.close()
        self.reset()

@autorepr
class LoggerFilelike(object):
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
    def __write__(self, message):
        self.logger(self.level, message)
    def __flush__(self):
        pass

@autorepr
class LogStderr(object):
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
    def __enter__(self):
        self.stderr = LoggerFilelike(self.logger, self.level)
        sys.stderr.flush()
        sys.stderr = self.stderr
    def __exit__(self, etype, value, trace):
        sys.stderr.flush()
        sys.stderr = sys.__stderr__
