#!/usr/bin/python3

import os
import sys

class RedirectStreams(object):
    def __init__(self, *, stdout=None, stderr = None, noclobber=False, use_temp=False):
        #Insert proper validation here
        self.stdout = stdout
        self.stderr = stderr
    def __enter__(self):
        self.stdout = sys.stdout if self.stdout is None else open(self.stdout, 'w')
        self.stderr = sys.stderr if self.stderr is None else open(self.stderr, 'w')
        sys.stdout.flush() ; sys.stderr.flush()
        sys.stdout, sys.stderr = self.stdout, self.stderr
    def __exit__(self, etype, value, trace):
        sys.stdout.flush() ; sys.stderr.flush()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    def __repr__(self):
        return "%s(stdout=%s, stderr=%s)" % (self.__class__.__qualname__, str(self.stdout), str(self.stderr))
